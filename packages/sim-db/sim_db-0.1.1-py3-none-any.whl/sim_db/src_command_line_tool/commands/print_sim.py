# -*- coding: utf-8 -*-
""" Print parameters of simulations ran or running, i.e. content of database.

Print the content of database with a number of possible restrictions.
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_package_root_to_path

import sim_db.src_command_line_tool.commands.helpers as helpers
import sqlite3
import argparse
import sys
import os


def command_line_arguments_parser(name_command_line_tool="sim_db",
                                  name_command="print_sim"):
    parser = argparse.ArgumentParser(
            description=('Print content in sim.db. If no arguments are '
                         'provided "-p default" is passed automatically.'),
            prog="{0} {1}".format(name_command_line_tool, name_command))
    parser.add_argument(
            '--id', '-i', type=int, nargs='+', help="List of ID's.")
    parser.add_argument(
            '--id_no_print',
            type=int,
            nargs='+',
            help="List of ID's not to print.")
    parser.add_argument(
            '-n', type=int, help="Number of row printed from the bottom up.")
    parser.add_argument(
            '--columns',
            '-c',
            type=str,
            nargs='+',
            default=None,
            help=("Name of the columns to print. All non empty columns are "
                  "printed by default."))
    parser.add_argument(
            '--columns_no_print',
            type=str,
            nargs='+',
            default=None,
            help="Name of the columns not to print.")
    parser.add_argument(
            '--col_by_num',
            type=int,
            nargs='+',
            default=None,
            help=("Number of the columns to print. All non empty columns are "
                  "printed by default."))
    parser.add_argument(
            '--where',
            '-w',
            default='id > -1',
            help=
            ("Add constraints to which columns to print. Must be a valid "
             "SQL (sqlite3) command when added after WHERE in a SELECT command."
             ))
    parser.add_argument(
            '--sort_by',
            default='id',
            help=
            ("What to sort the output by. Must be a valid SQL (sqlite3) "
             "command when added after ORDER BY in a SELECT search. Defalut is "
             "id."))
    parser.add_argument(
            '--column_names',
            action='store_true',
            help="Print name and type of all columns.")
    parser.add_argument(
            '--all_columns',
            action='store_true',
            help=("Print all columns. Otherwise only non empty columns are "
                  "printed."))
    parser.add_argument(
            '--no_headers',
            action='store_true',
            help="Print without any headers.")
    parser.add_argument(
            '--max_width',
            type=int,
            default=None,
            help=("Upper limit for the width of each column. Default is no "
                  "limit."))
    parser.add_argument(
            '--first_line',
            action='store_true',
            help="Print only the first line of any entry.")
    parser.add_argument(
            '--vertically',
            '-v',
            action='store_true',
            help="Print columns vertically.")
    parser.add_argument(
            '-p',
            type=str,
            default=None,
            help=
            ("Personal print configuration. Apply the print "
             "configuration in 'settings.txt' corresponding to the provided "
             "key string."))
    parser.add_argument(
            '--diff',
            '-d',
            action='store_true',
            help=
            ("Remove columns with the same value for all the "
             "simulations. This leaves only the parameters that are different "
             "between the simulations."))

    return parser


def get_personalized_print_config(key_string):
    settings = helpers.Settings()
    print_configs = settings.read('print_config')
    for line in print_configs:
        split_line = line.split(':')
        if len(split_line) > 1:
            if key_string.strip() == split_line[0].strip():
                return split_line[1].strip()
    return None


def select_command(db_cursor, args, column_names):
    if args.columns == None and args.col_by_num == None:
        columns = '*'
    else:
        columns = ""
        if args.columns != None:
            column_names = []
            for col in args.columns:
                columns += "{0}, ".format(col)
                column_names.append(col)
            columns = columns[:-2]
        if args.col_by_num != None:
            new_column_names = []
            for i in args.col_by_num:
                columns += "{0}, ".format(column_names[i])
                new_column_names.append(column_names[i])
            columns = columns[:-2]
            column_names = new_column_names
    if args.id == None:
        try:
            db_cursor.execute("SELECT {0} FROM runs WHERE {1} ORDER BY {2};"
                              .format(columns, args.where, args.sort_by))
        except sqlite3.OperationalError as e:
            if str(e) == "no such table: runs":
                print("There do NOT exists a database yet.\n"
                      "Try adding a simulation from a parameter file.")
                exit(1)
            else:
                raise e
        selected_output = db_cursor.fetchall()
    else:
        selected_output = []
        for i in args.id:
            restrictions = args.where + " AND id = {0}".format(i)
            try:
                db_cursor.execute(
                        "SELECT {0} FROM runs WHERE {1} ORDER BY {2};".format(
                                columns, restrictions, args.sort_by))
            except sqlite3.OperationalError as e:
                if str(e) == "no such table: runs":
                    print("There do NOT exists a database yet.\n"
                          "Try adding a simulation from a parameter file.")
                    exit(1)
                else:
                    raise e
            output = db_cursor.fetchall()
            if len(output) == 0:
                if (len(restrictions) > 12
                            and restrictions[0:12] == 'id > -1 AND '):
                    restrictions = restrictions[12:]
                print("There exists no entries in the database with: {0}"
                      .format(restrictions))
                exit(1)
            selected_output.append(output[0])

    selected_output = [list(row) for row in selected_output]
    if not args.all_columns and args.columns == None and args.col_by_num == None:
        selected_output, column_names = remove_empty_columns(
                selected_output, column_names)
    if args.columns_no_print != None:
        selected_output, column_names = remove_columns_not_to_print(
                selected_output, column_names, args.columns_no_print)
    if args.columns != None:
        column_names = args.columns
    if args.id_no_print != None:
        selected_output = remove_rows_not_to_print(selected_output,
                                                   args.id_no_print)
    n = args.n
    if n == None:
        n = len(selected_output)
    selected_output = selected_output[-n:]

    return selected_output, column_names


def remove_empty_columns(selected_output, column_names):
    if len(selected_output) == 0:
        return selected_output, column_names
    columns_to_remove = []
    for col in range(len(selected_output[0])):
        if all(elem is None for elem in [row[col] for row in selected_output]):
            columns_to_remove.append(col)
    n_deleted = 0
    for col in columns_to_remove:
        for row in selected_output:
            del row[col - n_deleted]
        del column_names[col - n_deleted]
        n_deleted += 1

    return selected_output, column_names


def remove_columns_not_to_print(selected_output, column_names,
                                columns_no_print):
    if len(selected_output) == 0:
        return selected_output, column_names
    columns_to_remove = []
    for i, col_name in enumerate(column_names):
        for col_name_no_print in columns_no_print:
            if col_name == col_name_no_print:
                columns_to_remove.append(i)
    n_deleted = 0
    for col in columns_to_remove:
        for row in selected_output:
            del row[col - n_deleted]
        del column_names[col - n_deleted]
        n_deleted += 1
    return selected_output, column_names


def remove_rows_not_to_print(selected_output, id_no_print):
    rows_to_remove = []
    for j in range(len(selected_output)):
        for i in id_no_print:
            if selected_output[j][0] == i:
                rows_to_remove.append(j)
    n_deleted = 0
    for j in rows_to_remove:
        del selected_output[j - n_deleted]
        n_deleted += 0
    return selected_output


def get_max_widths(selected_output, column_names, no_headers, extra_space):
    if len(selected_output) == 0:
        return selected_output
    widths = []
    for col in range(len(selected_output[0])):
        if no_headers:
            max_width = 0
        else:
            max_width = len(column_names[col])
        for row in range(len(selected_output)):
            if max_width < len(str(selected_output[row][col]).split('\n')[0]):
                max_width = len(str(selected_output[row][col]).split('\n')[0])
        widths.append(max_width + extra_space)
    return widths


def remove_columns_with_only_same_values(selected_output, column_names):
    column_indices_to_remove = []
    for column_index in range(len(column_names)):
        remove_column = True
        for row_index in range(len(selected_output) - 1):
            if (selected_output[row_index][column_index] !=
                        selected_output[row_index + 1][column_index]):
                remove_column = False
                break
        if remove_column:
            column_indices_to_remove.append(column_index)
    for i in reversed(column_indices_to_remove):
        del column_names[i]
        for row in range(len(selected_output)):
            del selected_output[row][i]
    return selected_output, column_names


def print_selected_parameters(selected_output, column_names, no_headers,
                              max_width, first_line):
    extra_space = 2
    widths = get_max_widths(selected_output, column_names, no_headers,
                            extra_space)
    if not no_headers:
        headers = ""
        total_width = 0
        for w, col in zip(widths, column_names):
            column_header = col + (w - len(col)) * " "
            if max_width and w > max_width:
                column_header = column_header[:max_width] + extra_space * " "
                total_width += max_width + extra_space
            else:
                total_width += w
            headers += column_header
        print(headers)
        print(total_width * "=")
    for row in selected_output:
        line = ""
        for w, value in zip(widths, row):
            column_value = str(value) + (w - len(str(value))) * " "
            if first_line:
                column_value = column_value.split('\n')[0]
            if max_width and w > max_width:
                column_value = column_value[:max_width] + extra_space * " "
            line += column_value
        print(line)


def print_selected_parameters_vertically(selected_output, column_names,
                                         no_headers, max_width, first_line):
    extra_space = 2
    new_columns = []
    widths = []
    n_new_columns = len(selected_output)
    new_columns = [[] for i in range(n_new_columns)]
    widths = n_new_columns * [0]
    for i, row in enumerate(selected_output):
        for value in row:
            if first_line:
                value = str(value).split('\n')[0]
            new_columns[i].append(str(value))
            width = len(str(value))
            if max_width != None and width > max_width:
                width = max_width
            if widths[i] < width:
                widths[i] = width

    width_headers = 0
    for column_name in column_names:
        width = len(column_name)
        if max_width != None and width > max_width:
            width = max_width
        if width_headers < width:
            width_headers = width

    n_new_rows = 0
    if len(new_columns) > 0:
        n_new_rows = len(new_columns[0])
    for i in range(n_new_rows):
        if not no_headers:
            sys.stdout.write(
                    "{1:<{0}}".format(width_headers + extra_space,
                                      column_names[i][:width_headers]))
        for j in range(n_new_columns):
            sys.stdout.write("{1:<{0}}".format(widths[j] + extra_space,
                                               new_columns[j][i][:widths[j]]))
        sys.stdout.write("\n\n")
        sys.stdout.flush()


def replace_element_in_list(the_list, element, replacement):
    for i in the_list:
        if i == element:
            the_list.remove(element)
            the_list.append(replacement)
    return the_list


def print_sim(name_command_line_tool="sim_db",
              name_command="print_sim",
              argv=None):
    if argv == None:
        args = command_line_arguments_parser(name_command_line_tool,
                                             name_command).parse_args(
                                                     ['-p', 'default'])
    else:
        args = command_line_arguments_parser(name_command_line_tool,
                                             name_command).parse_args(argv)
    if args.p != None:
        print_config = get_personalized_print_config(args.p)
        if print_config == None:
            print("No personalized print configuration with key string " \
                  + "'{0}' is found in settings.".format(args.p))
            exit(1)
        p_arg_keys = [
                key.strip('-') for key in print_config.split() if key[0] == '-'
        ]
        p_args = command_line_arguments_parser(name_command_line_tool,
                                               name_command).parse_args(
                                                       print_config.split())

        p_arg_keys = replace_element_in_list(p_arg_keys, 'v', 'vertically')
        p_arg_keys = replace_element_in_list(p_arg_keys, 'i', 'id')
        p_arg_keys = replace_element_in_list(p_arg_keys, 'c', 'columns')
        p_arg_keys = replace_element_in_list(p_arg_keys, 'w', 'where')

        for arg in vars(p_args):
            if arg in p_arg_keys:
                setattr(args, arg, getattr(p_args, arg))

    db = helpers.connect_sim_db()
    db_cursor = db.cursor()

    column_names, column_types = helpers.get_db_column_names_and_types(
            db_cursor)
    type_dict = dict(zip(column_names, column_types))

    selected_output, column_names = select_command(db_cursor, args,
                                                   column_names)

    if args.diff:
        selected_output, column_names = remove_columns_with_only_same_values(
                selected_output, column_names)

    if not args.vertically:
        print_selected_parameters(selected_output, column_names,
                                  args.no_headers, args.max_width,
                                  args.first_line)
    else:
        print_selected_parameters_vertically(selected_output, column_names,
                                             args.no_headers, args.max_width,
                                             args.first_line)

    if args.column_names:
        print("")
        print("Column names and types in database:")
        for col_name in column_names:
            col_type = type_dict[col_name]
            print("{0}, {1}".format(col_name, col_type))

    db.commit()
    db_cursor.close()
    db.close()


if __name__ == '__main__':
    print_sim("", sys.argv[0], sys.argv[1:])
