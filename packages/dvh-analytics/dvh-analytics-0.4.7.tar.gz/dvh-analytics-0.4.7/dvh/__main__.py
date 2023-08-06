#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:57 2017
@author: Dan Cutright, PhD
This is the main python file for command line implementation.
"""

from __future__ import print_function
from dicom_to_sql import dicom_to_sql
from sql_connector import DVH_SQL
from analysis_tools import DVH
from utilities import is_import_settings_defined, is_sql_connection_defined, Temp_DICOM_FileSet,\
    write_import_settings, write_sql_connection_settings, validate_import_settings, validate_sql_connection
from get_settings import get_settings
import os
from getpass import getpass
import argparse
from subprocess import call


SCRIPT_DIR = os.path.dirname(__file__)


if is_sql_connection_defined():
    try:
        DVH_SQL().initialize_database()
    except:
        print("Warning: could not initialize SQL database")


def settings(dir=False, sql=False):
    if not dir and not sql:
        set_import_settings()
        set_sql_connection_parameters()
    else:
        if dir:
            set_import_settings()
        if sql:
            set_sql_connection_parameters()


def test_import_sql_cnx_definitions():
    if not is_import_settings_defined() and not is_sql_connection_defined():
        print("ERROR: Import and SQL settings are not yet defined.",
              "Please run:\n",
              "    $ dvh settings_simple", sep='')
    elif not is_import_settings_defined():
        print("ERROR: Import settings are not yet defined.",
              "Please run:\n",
              "    $ dvh settings_simple --dir", sep='')
    elif not is_sql_connection_defined():
        print("ERROR: Invalid or empty SQL settings.",
              "Please run:\n",
              "    $ dvh settings_simple --sql", sep='')
    else:
        return True

    return False


def test_dvh_code():
    if test_import_sql_cnx_definitions():
        is_import_valid = validate_import_settings()
        is_sql_connection_valid = validate_sql_connection()
        if not is_import_valid and not is_sql_connection_valid:
            print("ERROR: Create the directories listed above or input valid directories.\n",
                  "ERROR: Cannot connect to SQL.\n",
                  "Please run:\n    $ dvh settings", sep='')
        elif not is_import_valid:
            print("ERROR: Create the directories listed above or input valid directories by running:\n",
                  "    $ dvh settings --dir", sep='')
        elif not is_sql_connection_valid:
            print("ERROR: Cannot connect to SQL.\n",
                  "Verify database is active and/or update SQL connection information with:\n",
                  "    $ dvh settings --sql", sep='')

        else:
            print("Importing test files")
            dicom_to_sql(start_path="test_files/",
                         force_update=False)

            print("Reading data from SQL DB with analysis_tools.py")
            test = DVH()

            print("Reading dicom information from test files with utilities.py (for plan review module)")
            test_files = Temp_DICOM_FileSet(start_path="test_files/")

            print("Deleting test data from SQL database")
            for i in range(0, test_files.count):
                cond_str = "mrn = '" + test_files.mrn[i]
                cond_str += "' and study_instance_uid = '" + test_files.study_instance_uid[i] + "'"
                DVH_SQL().delete_rows(cond_str)

            print("Tests successful!")


def get_import_settings_from_user():
    print("Please enter the full directory path for each category")

    print("This is where dicom files live before import.")
    inbox_file_path = raw_input('Inbox: ')

    print("This is where dicom files move to after import.")
    imported_file_path = raw_input('Imported: ')

    print("This is where dicom files to be reviewed live, but will not be imported.")
    review_file_path = raw_input('DVH Review: ')

    import_settings = {'inbox': str(inbox_file_path),
                       'imported': str(imported_file_path),
                       'review': str(review_file_path)}

    return import_settings


def get_sql_connection_parameters_from_user():

    print("Please enter the host address\n(defaults to 'localhost' if left empty)")
    host = raw_input('Host: ')
    if not host:
        host = 'localhost'

    print("Please enter the user name\n(leave empty for OS authentication)")
    user = raw_input('User: ')

    if user:
        print("Please enter the password, if any\n(will not display key strokes)")
        password = getpass('Password: ')

    print("Please enter the database name\n(defaults to dvh if empty)")
    dbname = raw_input('Database name: ')
    if not dbname:
        dbname = 'dvh'

    print("Please enter the database port\n(defaults to PostgreSQL default: 5432)")
    port = raw_input('Port: ')
    if not port:
        port = '5432'

    sql_connection_parameters = {'host': str(host),
                                 'dbname': str(dbname),
                                 'port': str(port)}

    if user:
        sql_connection_parameters['user'] = str(user)
        sql_connection_parameters['password'] = str(password)

    return sql_connection_parameters


def set_import_settings():
    config = get_import_settings_from_user()
    write_import_settings(config)


def set_sql_connection_parameters():
    config = get_sql_connection_parameters_from_user()
    write_sql_connection_settings(config)


def print_mrns():
    mrns = DVH_SQL().get_unique_values('plans', 'mrn')
    if len(mrns) == 0:
        print("No plans have been imported")

    printed_mrns = []
    for i in range(0, len(mrns)):
        current_mrn = mrns[i]
        if current_mrn not in printed_mrns:
            printed_mrns.append(current_mrn)
            print(current_mrn)


def initialize_default_import_settings_file():
    # Create default import settings file
    import_settings_path = get_settings('import')
    if not os.path.isfile(import_settings_path):
        if os.path.isfile('/this_is_running_in_docker'):
            write_import_settings({'inbox': '/dicom/inbox',
                                   'imported': '/dicom/imported',
                                   'review': '/dicom/review'})
        else:
            write_import_settings({'inbox': '',
                                   'imported': '',
                                   'review': ''})


def initialize_default_sql_connection_config_file():
    # Create default sql connection config file
    sql_connection_path = get_settings('sql')
    print(sql_connection_path)
    if not os.path.isfile(sql_connection_path):
        if os.path.isfile('/this_is_running_in_docker'):
            write_sql_connection_settings({'host': 'docker.for.mac.localhost',
                                           'user': 'postgres',
                                           'dbname': 'postgres',
                                           'port': '5432'})
        else:
            write_sql_connection_settings({'host': 'localhost',
                                           'dbname': 'dvh',
                                           'port': '5432'})


def main():
    parser = argparse.ArgumentParser(description='Command line interface for DVH Analytics')
    parser.add_argument('--sql',
                        help='Modify SQL connection settings',
                        default=False,
                        action='store_true')
    parser.add_argument('--dir',
                        help='Modify import directory settings',
                        default=False,
                        action='store_true')
    parser.add_argument('--start-path',
                        dest='start_path',
                        help='modify the start path for dicom import',
                        default=None)
    parser.add_argument('--force-update',
                        help='Import will add to SQL DB even if DB already contains data from dicom files',
                        default=False,
                        action='store_true')
    parser.add_argument('--allow-websocket-origin',
                        dest='allow_websocket_origin',
                        help='Allows Bokeh server to accept a non-default origin',
                        default=None)
    parser.add_argument('--port',
                        dest='port',
                        help='Initializes Bokeh server on a non-default port',
                        default=None)
    parser.add_argument('--bypass-sql-test',
                        help='Bypass the initial SQL connection test',
                        dest='bypass_sql_test',
                        default=False,
                        action='store_true')
    parser.add_argument('command', nargs='+', help='bar help')
    args = parser.parse_args()

    if args.command:

        if args.command[0] == 'settings_simple':
            if not args.sql and not args.dir:
                settings()
            else:
                if args.sql:
                    settings(sql=True)
                if args.dir:
                    settings(dir=True)

        elif args.command[0] == 'test':
            test_dvh_code()

        elif args.command[0] == 'echo':
            validate_sql_connection()

        elif args.command[0] == 'print_mrns':
            print_mrns()

        elif args.command[0] == 'import':

            # Set defaults
            start_path = False
            force_update = False

            if args.start_path:
                if os.path.isdir(args.start_path):
                    start_path = str(args.start_path)
                else:
                    print(args.start_path, 'is not a valid path', sep=' ')
            if args.force_update:
                force_update = True

            dicom_to_sql(start_path=start_path,
                         force_update=force_update)
        elif args.command[0] == 'run':

            command = ["bokeh", "serve"]

            if args.allow_websocket_origin:
                command.append("--allow-websocket-origin")
                command.append(args.allow_websocket_origin)
            if args.port:
                command.append("--port")  # Defaults to 5006
                command.append(args.port)
            if not args.allow_websocket_origin and not args.port:
                command.append("--show")

            command.append(SCRIPT_DIR)

            if not args.bypass_sql_test:
                if test_import_sql_cnx_definitions():
                    if DVH_SQL().is_sql_table_empty('DVHs'):
                        print("There is no data in your SQL table.")
                        print("You may import data from the admin view (use the 'admin' command instead of 'run'")

                    call(command)
                else:
                    print("Could not connect to SQL. You may need to update/initiate settings.")
                    print("Try running with 'settings' command instead of 'run'")
            else:
                call(command)

        elif args.command[0] == 'admin':
            command = ["bokeh", "serve", "--show", "--port"]
            if args.port:
                command.append(args.port)
            else:
                command.append("5007")
            if args.allow_websocket_origin:
                command.append("--allow-websocket-origin")
                command.append(args.allow_websocket_origin)

            file_name = 'admin.py'
            abs_file_path = os.path.join(SCRIPT_DIR, file_name)

            command.append(abs_file_path)

            if not args.bypass_sql_test:
                if test_import_sql_cnx_definitions():
                    call(command)
                else:
                    print("Could not connect to SQL. You may need to update/initiate settings.")
                    print("Try running with 'settings' command instead of 'admin'")
            else:
                call(command)

        elif args.command[0] == 'settings':

            initialize_default_import_settings_file()
            initialize_default_sql_connection_config_file()

            command = ["bokeh", "serve", "--show", "--port"]
            if args.port:
                command.append(args.port)
            else:
                command.append("5008")
            if args.allow_websocket_origin:
                command.append("--allow-websocket-origin")
                command.append(args.allow_websocket_origin)

            file_name = 'settings.py'
            abs_file_path = os.path.join(SCRIPT_DIR, file_name)

            command.append(abs_file_path)

            call(command)

        elif args.command[0] == 'create_tables':

            DVH_SQL().initialize_database()


if __name__ == '__main__':
    main()
