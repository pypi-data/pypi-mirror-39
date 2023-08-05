# -*- coding: utf-8 -*-
""" Read and modify settings."""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import sqlite3
import subprocess
import os
from sys import version_info, platform

# Update 'get_create_table_query' function in src/sim_db.c if ever changed.
default_db_columns = {
        'id': 'INTEGER PRIMARY KEY',
        'status': 'TEXT',
        'name': 'TEXT',
        'description': 'TEXT',
        'run_command': 'TEXT',
        'comment': 'TEXT',
        'results_dir': 'TEXT',
        'add_to_job_script': 'TEXT',
        'max_walltime': 'TEXT',
        'n_tasks': 'INTEGER',
        'job_id': 'INTEGER',
        'time_submitted': 'TEXT',
        'time_started': 'TEXT',
        'used_walltime': 'TEXT',
        'cpu_info': 'TEXT',
        'git_hash': 'TEXT',
        'commit_message': 'TEXT',
        'git_diff_stat': 'TEXT',
        'git_diff': 'TEXT',
        'sha1_executables': 'TEXT'
}


class Settings:
    settings_dict = {
            'parameter_files':
            '## Parameter filenames',
            'print_config':
            '## Personalized print configurations',
            'prefix_run_command':
            '## Prefix for \'run_command\' for multithreaded/core simultions',
            'which_job_scheduler':
            '### Which job scheduler',
            'n_cpus_per_node':
            '### Number of logical cpus per node',
            'memory_per_node':
            '### Memory per node',
            'account':
            '### Account',
            'email':
            '### Email for notifications',
            'add_to_job_script':
            '### Add to all job scripts submitted:',
    }

    def read(self, key_settings_dict, path_settings=None):
        setting_header = self.settings_dict[key_settings_dict]
        if path_settings == None:
            path_settings = os.path.join(get_dot_sim_db_dir_path(),
                                         'settings.txt')
        settings_file = open(path_settings, 'r')
        settings_found = []
        is_comment = False
        is_found = False
        for line in settings_file:
            line = line.strip()
            if (is_found and len(line) >= 2 and line[:2] == '##'):
                break
            if (len(line) > 0 and line[0] == '('):
                is_comment = True
            if (is_found and not is_comment and len(line) > 1):
                settings_found.append(line)
            if is_comment and len(line) > 0 and line[-1] == ')':
                is_comment = False
            if (len(line) >= len(setting_header)
                        and line[:len(setting_header)] == setting_header):
                is_found = True
        settings_file.close()
        if is_comment:
            raise ValueError("')' missing in 'settings.txt'.")
        return settings_found

    def add(self, key_settings_dict, setting, path_settings=None):
        setting = setting.strip()
        setting_header = self.settings_dict[key_settings_dict]
        if path_settings == None:
            path_settings = os.path.join(get_dot_sim_db_dir_path(),
                                         'settings.txt')
        settings_file = open(path_settings, 'r')
        settings_content = ''
        is_found = False
        is_comment = False
        is_added = False
        for line in settings_file.readlines():
            settings_content += line
            line = line.strip()
            if (is_found and line == setting):
                settings_file.close()
                return False
            if (is_found and len(line) >= 1 and line[:2] == '##'):
                is_found = False
            if (len(line) > 0 and line[0] == '('):
                is_comment = True
            if (is_found and not is_added and not is_comment):
                settings_content += setting + '\n'
                is_added = True
            if (is_comment and len(line) > 0 and line[-1] == ')'):
                is_comment = False
            if (len(line) >= len(setting_header)
                        and line[:len(setting_header)] == setting_header):
                is_found = True
        settings_file.close()
        settings_file = open(path_settings, 'w')
        settings_file.writelines(settings_content)
        settings_file.close()

    def remove(self, key_settings_dict, setting, path_settings=None):
        setting = setting.strip()
        setting_header = self.settings_dict[key_settings_dict]
        if path_settings == None:
            path_settings = os.path.join(get_dot_sim_db_dir_path(),
                                         'settings.txt')
        settings_file = open(path_settings, 'r')
        settings_content = ''
        is_header_found = False
        is_comment = False
        is_removed = False
        for line in settings_file.readlines():
            line = line.strip()
            if (is_header_found and len(line) >= 1 and line[:2] == '##'):
                is_header_found = False
            if (len(line) > 0 and line[0] == '('):
                is_comment = True
            if (is_header_found and not is_removed and not is_comment
                        and line.strip() == setting):
                is_removed = True
            else:
                settings_content += line + "\n"
            if (is_comment and len(line) > 0 and line[-1] == ')'):
                is_comment = False
            if (len(line) >= len(setting_header)
                        and line[:len(setting_header)] == setting_header):
                is_header_found = True
        settings_file.close()
        settings_file = open(path_settings, 'w')
        settings_file.writelines(settings_content)
        settings_file.close()

        return is_removed


def get_dot_sim_db_dir_path():
    """Return absolute path to '.sim_db/' directory or exits if unsuccessful.

    Search current and all parent directories for the '.sim_db/' directory,
    and returns the absoluth path to the '.sim_db/' directory. Path does NOT 
    end with '/'.
    """

    path_dir = os.getcwd()
    prev_path_dir = ""
    while path_dir != prev_path_dir:
        if os.path.isdir(os.path.join(path_dir, ".sim_db")):
            return os.path.join(path_dir, ".sim_db")
        prev_path_dir = path_dir
        path_dir = os.path.dirname(path_dir)

    print("Could NOT find '.sim_db/' in this or any parent directories.")
    print("Run '$ init' in the project's root directory.")
    exit(1)


def connect_sim_db(full_path_sim_db=None):
    if (full_path_sim_db == None):
        full_path_sim_db = os.path.join(get_dot_sim_db_dir_path(), 'sim.db')
    return sqlite3.connect(full_path_sim_db)


def get_db_column_names_and_types(db_cursor):
    table_info = db_cursor.execute("PRAGMA table_info('runs')")
    column_names = []
    column_types = []
    for row in table_info:
        column_names.append(row[1])
        column_types.append(row[2])
    return column_names, column_types


def get_run_command(db_cursor, db_id, n_tasks=None):
    db_cursor.execute(
            "SELECT run_command, n_tasks FROM runs WHERE id={0};".format(
                    db_id))
    run_command, n_tasks_database = db_cursor.fetchall()[0]
    if n_tasks == None:
        n_tasks = n_tasks_database

    if n_tasks == None:
        n_tasks = 1
    elif n_tasks > 1:
        settings = Settings()
        prefix_run_command = ""
        for prefix in settings.read('prefix_run_command'):
            prefix_run_command += prefix + ' '
        run_command = prefix_run_command + run_command

    proj_root_dir = os.path.abspath(
            os.path.join(get_dot_sim_db_dir_path(), os.pardir))
    if os.sep == '/':
        space_escaped = '\ '
    else:
        space_escaped = ' '
    run_command = run_command.replace(
            ' root/', ' ' + proj_root_dir.replace(' ', space_escaped) + os.sep)
    run_command = run_command.replace(' # ', " {0} ".format(n_tasks))
    run_command = run_command + " --id {0}".format(db_id)
    run_command = run_command + ' --path_proj_root "{0}"'.format(proj_root_dir)

    return run_command


def get_cpu_and_mem_info():
    if platform == 'linux' or platform == 'linux2' or platform == 'linux3':
        proc = subprocess.Popen(
                ["lscpu"],
                stdout=subprocess.PIPE,
                stderr=open(os.devnull, 'w'),
                shell=True)
        (out, err) = proc.communicate()
        cpu_info = ""
        wanted_info = [
                'Model name:', 'CPU(s):', 'Thread(s) per core:',
                'Core(s) per socket:', 'L1d cache:', 'L1i cache:', 'L2 cache:',
                'L3 cache:'
        ]
        for info in wanted_info:
            for lscpu_line in out.decode('ascii', 'replace').splitlines():
                if info == lscpu_line[0:len(info)]:
                    cpu_info += lscpu_line + '\n'

        proc = subprocess.Popen(
                [
                        "cat /sys/devices/system/cpu/cpu0/cache/index0/coherency_line_size"
                ],
                stdout=subprocess.PIPE,
                stderr=open(os.devnull, 'w'),
                shell=True)
        (out, err) = proc.communicate()
        if out != None:
            cpu_info += "coherency_line_size: " + out.decode(
                    'ascii', 'replace') + '\n'

        proc = subprocess.Popen(
                ["free -g -t"],
                stdout=subprocess.PIPE,
                stderr=open(os.devnull, 'w'),
                shell=True)
        (out, err) = proc.communicate()
        if out != None:
            memory = out.decode('ascii',
                                'replace').splitlines()[1].split()[0:2]
            cpu_info += memory[0] + ' ' + memory[1] + '\n'

        return cpu_info

    elif platform == 'darwin':
        proc = subprocess.Popen(
                ["sysctl -a"],
                stdout=subprocess.PIPE,
                stderr=open(os.devnull, 'w'),
                shell=True)
        (out, err) = proc.communicate()
        cpu_info = ""
        wanted_info = [
                'machdep.cpu.brand_string:', 'machdep.cpu.core_count:',
                'machdep.cpu.thread_count:', 'hw.cachelinesize:',
                'hw.l1icachesize:', 'hw.l1dcachesize:', 'hw.l2cachesize:',
                'hw.l3cachesize:', 'hw.memsize:'
        ]
        for info in wanted_info:
            for lscpu_line in out.decode('ascii', 'replace').splitlines():
                if info == lscpu_line[0:len(info)]:
                    cpu_info += lscpu_line + '\n'
        return cpu_info
    else:
        return "Not Linux or Mac"


def user_input(message):
    """Call raw_input for python 2 and input for python 3."""
    if version_info[0] < 3:
        return raw_input(message)
    else:
        return input(message)


def if_unicode_convert_to_str(value):
    """Return value. Convert to string only if python 2 and value is unicode."""
    if version_info[0] < 3:
        if type(value) == unicode:
            return value.encode('ascii', 'backslashreplace')
    else:
        return value
