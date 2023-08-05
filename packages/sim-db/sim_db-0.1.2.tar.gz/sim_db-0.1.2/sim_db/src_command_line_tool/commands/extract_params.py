# -*- coding: utf-8 -*-
""" Extract the parameters from the database to a parameter file.

The parameter file can be used to add a new equal simulation, but more usefully
modified to run a slightly different simulation.
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_package_root_to_path

import sim_db.src_command_line_tool.commands.helpers as helpers
import sqlite3
import argparse
import sys
import os.path

no_extract_columns = {
        'id', 'status', 'comment', 'time_submitted', 'time_started',
        'used_walltime', 'job_id', 'cpu_info', 'git_hash', 'commit_message',
        'git_diff_stat', 'git_diff', 'sha1_executables'
}


def command_line_arguments_parser(name_command_line_tool="sim_db",
                                  name_command="extract_params"):
    parser = argparse.ArgumentParser(
            description='Extract parameter file from sim.db.',
            prog="{0} {1}".format(name_command_line_tool, name_command))
    parser.add_argument(
            '--id',
            '-i',
            type=int,
            required=True,
            help=("<Required> ID of the simulation which parameter one wish "
                  "to extract."))
    parser.add_argument(
            '--filename',
            '-f',
            type=str,
            default=None,
            help="Name of parameter file generated.")
    parser.add_argument(
            '--default_file',
            '-d',
            action='store_true',
            help=
            ("Write parameters to the first of the 'Parameter filenames' "
             "in settings.txt. Ask for confirmation if file exists already."))
    parser.add_argument(
            '--also_empty',
            action='store_true',
            help=("Also extract empty paramters. Default is to not extract "
                  "empty parameters and default columns that are not input "
                  "parameters."))
    parser.add_argument(
            '--all',
            action='store_true',
            help=
            ("Extract all parameters. Default is to not extract empty "
             "parameters and default columns that are not input parameters."))

    return parser


def get_param_type_as_string(col_type, value):
    if col_type == 'INTEGER':
        return 'int'
    elif col_type == 'REAL':
        return 'float'
    elif col_type == 'TEXT':
        if value == 'True' or value == 'False':
            return 'bool'
        value_split = value.split('[')
        if len(value_split) > 1:
            return value_split[0] + ' array'
        else:
            return 'string'
    else:
        raise ValueError()


def extract_params(name_command_line_tool="sim_db",
                   name_command="extract_params",
                   argv=None):
    args = command_line_arguments_parser(name_command_line_tool,
                                         name_command).parse_args(argv)

    is_printing_parameters = True
    if args.default_file:
        param_files = helpers.Settings().read('parameter_files')
        if len(param_files) == 0:
            print("ERROR: No '--filename' provided and no " \
                    + "'Parameters files' in settings.txt."
                  )
            exit()
        else:
            filename = param_files[0]
        if os.path.exists(filename):
            answer = helpers.user_input(
                    "Would you like to overwrite '{0}'? (y/n)".format(
                            filename))
            if answer != 'y' and answer != 'Y' and answer != 'yes' and answer != 'Yes':
                exit()
        print("Extracts parameters to '{0}'.".format(filename))
        is_printing_parameters = False
    elif args.filename != None:
        filename = args.filename
        is_printing_parameters = False
    if not is_printing_parameters:
        params_file = open(filename, 'w')

    db = helpers.connect_sim_db()
    db_cursor = db.cursor()

    db_cursor.execute("SELECT * FROM runs WHERE id={0}".format(args.id))
    extracted_row = db_cursor.fetchall()

    column_names, column_types = helpers.get_db_column_names_and_types(
            db_cursor)

    for col_name, col_type, value in zip(column_names, column_types,
                                         extracted_row[0]):
        if col_name in no_extract_columns:
            skip = True
        else:
            skip = False

        if ((args.also_empty or value != None) and not skip) or args.all:
            line = col_name
            param_type = get_param_type_as_string(col_type, value)
            line += " ({0}): ".format(param_type)
            if param_type[-3:] == 'ray':
                value = '[' + value.split('[')[1]
            line += str(value).replace(':', ';') + '\n'
            if is_printing_parameters:
                print(line)
            else:
                params_file.write(line)
    if not is_printing_parameters:
        params_file.close()

    db.commit()
    db_cursor.close()
    db.close()


if __name__ == '__main__':
    extract_params("", sys.argv[0], sys.argv[1:])
