# -*- coding: utf-8 -*-
"""Read and write parameters, results and metadata to the 'sim_db' database."""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import sim_db.src_command_line_tool.commands.helpers as helpers
import sim_db.src_command_line_tool.commands.update_sim as update_sim
import sim_db.src_command_line_tool.commands.add_column as add_column
import sqlite3
import argparse
import subprocess
import time
import hashlib
import os


class SimDB:
    def __init__(self, store_metadata=True, db_id=None):
        """Add metadata to database and note start time.

        Update 'time_started', 'git_hash', 'commit_message', 'git_diff_stat'
        and 'git_diff'.

        'time_started' used the format: 'Year-Month-Date_Hours-Minutes-Seconds'.

        :param store_metadata: If False, no metadata is added to the database.
            Typically used when postprocessing (visualizing) data from a
            simulation.
        :type store_metadata: bool
        :param db_id: ID of the row in the database to update. If it is
            'None', then it is read from the last argument passed to the program
            after option '--id'.
        :type db_id: int
        """
        self.store_metadata = store_metadata
        self.id, self.path_proj_root = self.__read_from_command_line_arguments(
                db_id)
        self.start_time = time.time()

        if self.store_metadata:
            self.write(column="status", value="running")
            self.write('time_started', self.get_date_and_time_as_string())

        if self.store_metadata and self.__is_a_git_project():
            if os.sep == '/':
                path_proj_root = self.path_proj_root.replace(' ', '\ ')
            else:
                path_proj_root = self.path_proj_root
            proc = subprocess.Popen(
                    ["cd {0}; git rev-parse HEAD".format(path_proj_root)],
                    stdout=subprocess.PIPE,
                    stderr=open(os.devnull, 'w'),
                    shell=True)
            (out, err) = proc.communicate()
            self.write(column="git_hash", value=out.decode('ascii', 'replace'))

            proc = subprocess.Popen(
                    [
                            "cd {0}; git log -n 1 --format=%B HEAD".format(
                                    path_proj_root)
                    ],
                    stdout=subprocess.PIPE,
                    stderr=open(os.devnull, 'w'),
                    shell=True)
            (out, err) = proc.communicate()
            self.write(
                    column="commit_message",
                    value=out.decode('ascii', 'replace'))

            proc = subprocess.Popen(
                    ["cd {0}; git diff HEAD --stat".format(path_proj_root)],
                    stdout=subprocess.PIPE,
                    stderr=open(os.devnull, 'w'),
                    shell=True)
            (out, err) = proc.communicate()
            self.write(
                    column="git_diff_stat",
                    value=out.decode('ascii', 'replace'))

            proc = subprocess.Popen(
                    ["cd {0}; git diff HEAD".format(path_proj_root)],
                    stdout=subprocess.PIPE,
                    stderr=open(os.devnull, 'w'),
                    shell=True)
            (out, err) = proc.communicate()
            out = out.decode('ascii', 'replace')
            if len(out) > 3000:
                warning = "WARNING: Diff limited to first 3000 characters.\n"
                out = warning + '\n' + out[0:3000] + '\n\n' + warning
            self.write(column="git_diff", value=out)

    def read(self, column, db_id=None, check_type_is=''):
        """Read parameter with id 'db_id' and column 'column' from the database.

        :param column: Name of the column the parameter is read from.
        :type column: str
        :param db_id: ID of the row the parameter is read from. If it is 
            'None', then it is read from arguments passed to the program after 
            the option '--id'.
        :type db_id: int
        :param check_type_is: Throws ValueError if type does not match 
            'check_type_is'.The valid types the strings 'int', 'float', 'bool',
            'string' and 'int/float/bool/string array' or the types int, float, 
            bool, str and list.
        :raises: ValueError - if return type does not match 'check_type_is'.
        """
        if db_id == None:
            db_id = self.id

        db = helpers.connect_sim_db()
        db_cursor = db.cursor()

        column_names, column_types = helpers.get_db_column_names_and_types(
                db_cursor)
        if column not in column_names:
            print("Column, {0}, is NOT a column in the database, 'sim.db'.".
                  format(column))
            exit()

        db_cursor.execute("SELECT {0} FROM runs WHERE id={1}".format(
                column, db_id))
        value = db_cursor.fetchone()[0]

        value = self.__check_type(db_cursor, check_type_is, column, value)

        db.commit()
        db_cursor.close()
        db.close()

        return value

    def write(self, column, value, type_of_value='', db_id=None):
        """Write to entry with id 'db_id' and column 'column' from the database.

        If 'column' does not exists, a new is added.

        :param column: Name of the column the parameter is read from.
        :type column: str
        :param value: New value of the specified entry in the database.
        :param db_id: ID of the row the parameter is read from. If it is
            'None', then it is read from arguments passed to the program after
            the option '--id'.
        :type db_id: int
        :param type_of_value: Needed if column does note exists or if
            value is empty list. The valid types the strings 'int', 'float',
            'bool', 'string' and 'int/float/bool/string array' or the types int,
            float, bool and str.
        :type type_of_value: str or type
        :raises: ValueError - if column exists, but type does not match, or 
            empty list is passed without type_of_value given.
        """
        if db_id == None:
            db_id = self.id

        db = helpers.connect_sim_db()
        db_cursor = db.cursor()
        column_names, column_types = helpers.get_db_column_names_and_types(
                db_cursor)
        type_dict = dict(zip(column_names, column_types))
        if column in column_names:
            self.__check_type(db_cursor, type_of_value, column)
        else:
            if type_of_value == '':
                print("ERROR: Column {0} does not exists in ".format(column) \
                        + "database and 'type_of_value' must be provided for " \
                        + "it to be added.")
                exit()
            if type_of_value == int:
                type_of_value = 'int'
            if type_of_value == float:
                type_of_value = 'float'
            if type_of_value == bool:
                type_of_value = 'bool'
            if type_of_value == str:
                type_of_value = 'string'
            add_column.add_column(
                    argv=["--column", column, "--type", type_of_value])

        value_string = self.__convert_to_value_string(value, type_of_value)
        if value_string != None:
            value_string = self.__escape_quote_with_two_quotes(value_string)
        update_sim.update_sim(argv=[
                "--id",
                str(db_id), "--columns", column, "--value", value_string
        ])

    def get_id(self):
        """Return 'ID' of the connected simulation."""
        return self.id

    def get_path_proj_root(self):
        """Return the path to the root directory of the project.

        The project's root directory is assumed to be where the '.sim_db/'
        directory is located.
        """
        return self.path_proj_root

    def make_unique_subdir(self, path_directory):
        """Make a unique subdirectory in 'name_result_directory'.

        The subdirectory will be named date_time_name_id and is intended to
        store results in.

        :param path_directory: Path to directory of which to make a 
            subdirectory. If 'path_directory' starts with 'root/', that part 
            will be replaced by the full path of the root directory of the 
            project.
        :type path_directory: str
        :returns: Full path to new subdirectory.
        :rtype: str
        """
        if (len(path_directory) >= 5 and path_directory[0:5] == 'root/'):
            path_directory = os.path.join(self.path_proj_root,
                                          path_directory[5:])
        subdir = os.path.join(path_directory,
                              self.get_date_and_time_as_string())
        subdir += '_' + self.read('name') + '_' + str(self.id)
        subdir = os.path.abspath(os.path.realpath(subdir))
        if os.path.exists(subdir):
            subdir += "__no2"
        while (os.path.exists(subdir)):
            i = subdir.rfind("_no")
            subdir = subdir[:i + 4] + str(int(subdir[i + 4:]) + 1)
        os.mkdir(subdir)

        if self.store_metadata:
            self.write(column="results_dir", value=subdir)

        return subdir

    def update_sha1_executables(self, paths_executables):
        """Update the 'sha1_executable' column in the database.

        Sets the entry to the sha1 of all the executables. The order will
        affect the value.

        :param paths_executables: List of full paths to executables.
        :type paths_executables: [str]
        """
        sha1 = hashlib.sha1()
        for executable in executables:
            with open(executable, 'r') as executable_file:
                sha1.update(executable_file.read())
        self.write('sha1_executables', sha1)

    def end(self):
        """Add metadata for 'used_walltime' and update 'status' to 'finished'."""
        if self.store_metadata:
            used_time = time.time() - self.start_time
            used_walltime = "{0}h {1}m {2}s".format(
                    int(used_time / 3600), int(used_time / 60), used_time % 60)
            self.write('used_walltime', used_walltime)
            self.write('status', 'finished')

    def __read_from_command_line_arguments(self, db_id):
        path_proj_root = None
        if db_id == None:
            parser = argparse.ArgumentParser()
            parser.add_argument(
                    '--id',
                    '-i',
                    type=int,
                    default=None,
                    required=True,
                    help=("<Required> ID of parameters in the database used "
                          "to run the simulation."))
            parser.add_argument(
                    '--path_proj_root',
                    '-p',
                    type=str,
                    default=None,
                    help="Path to the root directory of the project.")
            args, unknowns = parser.parse_known_args()
            db_id = args.id
            if args.path_proj_root != None:
                path_proj_root = os.path.abspath(args.path_proj_root)
        if (path_proj_root == None):
            path_proj_root = os.path.dirname(helpers.get_dot_sim_db_dir_path())
        else:
            if path_proj_root[-1] == '/':
                path_proj_root = path_proj_root[:-1]
        if (db_id == None):
            ValueError("'db_id' is NOT provided to SimDB(db_id=None). If not "
                       "passed as function parameters, then '--id ID' must be "
                       "passed to program as command line arguments.")
        return (db_id, path_proj_root)

    def __check_type(self, db_cursor, check_type_is, column, value=None):
        column_names, column_types = helpers.get_db_column_names_and_types(
                db_cursor)
        type_dict = dict(zip(column_names, column_types))
        type_of_value = type_dict[column]

        if ((check_type_is == 'int' or check_type_is == int)
                    and type_of_value == 'INTEGER'):
            correct_type = True
        elif ((check_type_is == 'float' or check_type_is == float)
              and type_of_value == 'REAL'):
            correct_type = True
        elif (type_of_value == 'TEXT' and value != None):
            value, correct_type = self.__convert_text_to_correct_type(
                    value, check_type_is)
        elif (type_of_value == 'TEXT' and value == None
              and (check_type_is == 'string' or check_type_is == str
                   or check_type_is == 'bool' or check_type_is == bool
                   or check_type_is == list or check_type_is == 'int array'
                   or check_type_is == 'float array'
                   or check_type_is == 'bool array'
                   or check_type_is == 'string array')):
            correct_type = True
        else:
            correct_type = False

        if not correct_type and check_type_is != '':
            raise ValueError("The type is NOT {0}.".format(check_type_is))

        return value

    def __convert_text_to_correct_type(self, value, check_type_is):
        correct_type = False
        value_split = value.split('[')
        if value == "True":
            value = True
            if (check_type_is == 'bool' or check_type_is == bool):
                correct_type = True
        elif value == "False":
            value = False
            if (check_type_is == 'bool' or check_type_is == bool):
                correct_type = True
        elif len(value_split) == 1:
            if (check_type_is == 'string' or check_type_is == str):
                correct_type = True
        else:
            value = []
            if value_split[0].strip() == 'int':
                if (check_type_is == 'int array' or check_type_is == list):
                    correct_type = True
                for element in value_split[1].split(']')[0].split(','):
                    value.append(int(element))
            elif value_split[0].strip() == 'float':
                if (check_type_is == 'float array' or check_type_is == list):
                    correct_type = True
                for element in value_split[1].split(']')[0].split(','):
                    value.append(float(element))
            elif value_split[0].strip() == 'string':
                if (check_type_is == 'string array' or check_type_is == list):
                    correct_type = True
                for i, element in enumerate(
                        value_split[1].split(']')[0].split(',')):
                    if i > 0 and len(element) > 0 and element[0] == ' ':
                        element = element[1:]
                    value.append(str(element))
            elif value_split[0].strip() == 'bool':
                if (check_type_is == 'bool array' or check_type_is == list):
                    correct_type = True
                for i, element in enumerate(
                        value_split[1].split(']')[0].split(',')):
                    if i > 0 and len(element) > 0 and element[0] == ' ':
                        element = element[1:]
                    if element == 'True':
                        element = True
                    elif element == 'False':
                        element = False
                    else:
                        correct_type = False
                    value.append(element)
            else:
                correct_type = False
        return value, correct_type

    def __convert_to_value_string(self, value, type_of_value):
        if type(value) == int or type(value) == float or type(value) == str:
            return str(value)
        elif type(value) == bool:
            if value:
                return "True"
            else:
                return "False"
        elif type(value) == list:
            if len(value) > 0:
                if type(value[0]) == int:
                    value_string = "int["
                elif type(value[0]) == float:
                    value_string = "float["
                elif type(value[0]) == str:
                    value_string = "string["
                elif type(value[0]) == bool:
                    value_string = "bool["
                for element in value:
                    if type(value[0]) == bool:
                        if element:
                            element = "True"
                        else:
                            element = "False"
                    value_string += str(element) + ", "
                value_string = value_string[:-2] + "]"
                return value_string
            else:
                if type_of_value == 'int array':
                    value_string = "int[]"
                elif type_of_value == 'float array':
                    value_string = "float[]"
                elif type_of_value == 'string array':
                    value_string = "string[]"
                elif type_of_value == 'bool array':
                    value_string = "bool[]"
                else:
                    raise ValueError(
                            "The type_of_value must be set to 'int array', "
                            "'float array', 'string array' or 'bool array' "
                            "when a empty list is passed to SimDB.write().")
                return value_string

    def __is_a_git_project(self):
        directory = self.path_proj_root
        prev_dir = ""
        while directory != prev_dir:
            if os.path.exists(os.path.join(directory, ".git")):
                return True
            prev_dir = directory
            directory = os.path.dirname(directory)
        return False

    def __escape_quote_with_two_quotes(self, string):
        escaped_string = ""
        for letter in string:
            if letter == "'":
                escaped_string += "''"
            else:
                escaped_string += letter
        return escaped_string

    def get_date_and_time_as_string(self):
        """Return data and time as 'Year-Month-Date_Hours-Minutes-Seconds'."""
        return time.strftime("%Y-%b-%d_%H-%M-%S")


def add_empty_sim():
    """Add an empty entry into the database and return its 'ID'."""
    db = helpers.connect_sim_db()
    db_cursor = db.cursor()
    default_db_columns = ""
    for key in helpers.default_db_columns:
        default_db_columns += key + " " + str(
                helpers.default_db_columns[key]) + ", "
    default_db_columns = default_db_columns[:-2]
    db_cursor.execute("CREATE TABLE IF NOT EXISTS runs ({0});".format(
            default_db_columns))
    db_cursor.execute("INSERT INTO runs DEFAULT VALUES")
    db_id = db_cursor.lastrowid
    db.commit()
    db_cursor.close()
    db.close()

    return db_id


def delete_sim(db_id):
    """Delete simulation from database with 'ID' db_id."""
    db = helpers.connect_sim_db()
    db_cursor = db.cursor()
    db_cursor.execute("DELETE FROM runs WHERE id = {0}".format(db_id))
    db_id = db_cursor.lastrowid
    db.commit()
    db_cursor.close()
    db.close()
