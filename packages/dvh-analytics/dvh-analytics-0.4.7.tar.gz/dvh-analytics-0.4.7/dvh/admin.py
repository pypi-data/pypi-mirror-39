#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 13:43:28 2017
@author: nightowl
"""

from __future__ import print_function
from future.utils import listvalues
from utilities import is_import_settings_defined, is_sql_connection_defined, validate_sql_connection, \
    recalculate_ages, update_min_distances_in_db, update_treatment_volume_overlap_in_db, update_volumes_in_db, \
    update_surface_area_in_db, load_options, update_centroid_in_db, update_spread_in_db, update_cross_section_in_db,\
    update_dist_to_ptv_centroids_in_db, get_csv
import os
from os.path import dirname, join
from datetime import datetime
from roi_name_manager import DatabaseROIs, clean_name
from sql_connector import DVH_SQL
from dicom_to_sql import dicom_to_sql, rebuild_database
from bokeh.models.widgets import Select, Button, Tabs, Panel, TextInput, RadioButtonGroup,\
    Div, MultiSelect, TableColumn, DataTable, CheckboxGroup, PasswordInput
from bokeh.layouts import layout, row, column
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, LabelSet, Range1d, Slider, CustomJS, Spacer
import auth
import time
import options
from get_settings import get_settings, parse_settings_file
from shutil import copyfile


options = load_options(options)


# This depends on a user defined function in dvh/auth.py.  By default, this returns True
# It is up to the user/installer to write their own function (e.g., using python-ldap)
# Proper execution of this requires placing Bokeh behind a reverse proxy with SSL setup (HTTPS)
# Please see Bokeh documentation for more information
ACCESS_GRANTED = not options.AUTH_USER_REQ

# Create empty Bokeh data sources
query_source = ColumnDataSource(data=dict())
query_data_csv = ColumnDataSource(data=dict(text=[]))
baseline_source = ColumnDataSource(data=dict(mrn=[]))
roi_map_table_source = ColumnDataSource(data=dict(institutional_roi=[], physician_roi=[], variation=[]))

directories = {}
config = {}
categories = ["Institutional ROI", "Physician", "Physician ROI", "Variation"]
operators = ["Add", "Delete", "Rename"]


def load_directories():
    global directories
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Get Import settings
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if is_import_settings_defined():
        directories = parse_settings_file(get_settings('import'))
    else:
        directories = {'inbox': '',
                       'imported': '',
                       'review': ''}


def load_sql_settings():
    global config
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Get SQL settings
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if is_sql_connection_defined():
        config = parse_settings_file(get_settings('sql'))

        if 'user' not in list(config):
            config['user'] = ''
            config['password'] = ''

    else:
        config = {'host': 'localhost',
                  'dbname': 'dvh',
                  'port': '5432',
                  'user': '',
                  'password': ''}


# Load Settings
load_directories()
load_sql_settings()

# Load ROI map
db = DatabaseROIs()


###############################
# Institutional roi functions
###############################
def delete_institutional_roi():
    db.delete_institutional_roi(select_institutional_roi.value)
    new_options = db.get_institutional_rois()
    select_institutional_roi.options = new_options
    select_institutional_roi.value = new_options[0]


def add_institutional_roi():
    new = clean_name(input_text.value)
    if len(new) > 50:
        new = new[0:50]
    if new and new not in db.get_institutional_rois():
        db.add_institutional_roi(new)
        select_institutional_roi.options = db.get_institutional_rois()
        select_institutional_roi.value = new
        input_text.value = ''
        update_select_unlinked_institutional_roi()


def select_institutional_roi_change(attr, old, new):
    update_input_text()


def update_institutional_roi_select():
    new_options = db.get_institutional_rois()
    select_institutional_roi.options = new_options
    select_institutional_roi.value = new_options[0]


def rename_institutional_roi():
    new = clean_name(input_text.value)
    db.set_institutional_roi(new, select_institutional_roi.value)
    update_institutional_roi_select()
    select_institutional_roi.value = new


##############################################
# Physician ROI functions
##############################################
def update_physician_roi(attr, old, new):
    select_physician_roi.options = db.get_physician_rois(new)
    try:
        select_physician_roi.value = select_physician_roi.options[0]
    except KeyError:
        pass


def add_physician_roi():
    new = clean_name(input_text.value)
    if len(new) > 50:
        new = new[0:50]
    if new and new not in db.get_physicians():
        db.add_physician_roi(select_physician.value, 'uncategorized', new)
        select_physician_roi.options = db.get_physician_rois(select_physician.value)
        select_physician_roi.value = new
        input_text.value = ''
    elif new in db.get_physicians():
        input_text.value = ''


def delete_physician_roi():
    if select_physician.value not in {'DEFAULT', ''}:
        db.delete_physician_roi(select_physician.value, select_physician_roi.value)
        select_physician_roi.options = db.get_physician_rois(select_physician.value)
        select_physician_roi.value = db.get_physician_rois(select_physician.value)[0]


def select_physician_roi_change(attr, old, new):
    update_variation()
    update_input_text()
    update_roi_map_source_data()
    update_select_unlinked_institutional_roi()


def rename_physician_roi():
    new = clean_name(input_text.value)
    db.set_physician_roi(new, select_physician.value, select_physician_roi.value)
    update_physician_roi_select()
    select_physician_roi.value = new


##############################
# Physician functions
##############################
def update_physician_select():
    new_options = db.get_physicians()
    new_options.sort()
    select_physician.options = new_options
    select_physician.value = new_options[0]
    update_input_text()
    update_roi_map_source_data()


def add_physician():
    new = clean_name(input_text.value).upper()
    if len(new) > 50:
        new = new[0:50]
    if new and new not in db.get_physicians():
        input_text.value = ''
        db.add_physician(new)
        select_physician.options = db.get_physicians()
        try:
            select_physician.value = new
        except KeyError:
            pass
    elif new in db.get_physicians():
        input_text.value = ''


def delete_physician():
    if select_physician.value != 'DEFAULT':
        db.delete_physician(select_physician.value)
        new_options = db.get_physicians()
        select_physician.options = new_options
        select_physician.value = new_options[0]


def select_physician_change(attr, old, new):
    update_physician_roi_select()
    update_input_text()
    update_select_unlinked_institutional_roi()
    update_uncategorized_variation_select()
    update_ignored_variations_select()
    update_roi_map_table_source()


def rename_physician():
    new = clean_name(input_text.value)
    db.set_physician(new, select_physician.value)
    update_physician_select()
    select_physician.value = new


###################################
# Physician ROI Variation functions
###################################
def update_physician_roi_select():
    new_options = db.get_physician_rois(select_physician.value)
    select_physician_roi.options = new_options
    select_physician_roi.value = new_options[0]
    update_input_text()
    update_roi_map_source_data()


def update_variation():
    select_variation.options = db.get_variations(select_physician.value,
                                                 select_physician_roi.value)
    select_variation.value = select_variation.options[0]


def add_variation():
    new = clean_name(input_text.value)
    if len(new) > 50:
        new = new[0:50]
    if new and new not in db.get_all_variations_of_physician(select_physician.value):
        db.add_variation(select_physician.value,
                         select_physician_roi.value,
                         new)
        select_variation.value = new
        input_text.value = ''
        update_variation()
        select_variation.value = new
    elif new in db.get_variations(select_physician.value,
                                  select_physician_roi.value):
        input_text.value = ''


def delete_variation():
    if select_variation.value != select_physician_roi.value:
        db.delete_variation(select_physician.value, select_physician_roi.value, select_variation.value)
        new_options = db.get_variations(select_physician.value, select_physician_roi.value)
        select_variation.options = new_options
        select_variation.value = new_options[0]


def select_variation_change(attr, old, new):
    update_input_text()


################
# Misc functions
################
def rename_variation():
    new = clean_name(input_text.value)
    db.set_variation(new, select_physician.value, select_physician_roi.value, select_variation.value)
    update_variation()
    select_variation.value = new


def update_input_text_title():
    input_text.title = operators[operator.active] + " " + categories[category.active] + ":"
    update_action_text()


def update_input_text_value():
    category_map = {0: select_institutional_roi.value,
                    1: select_physician.value,
                    2: select_physician_roi.value,
                    3: select_variation.value}
    if operator.active != 0:
        input_text.value = category_map[category.active]
    elif operator.active == 0 and category.active == 3:
        input_text.value = select_uncategorized_variation.value
    else:
        input_text.value = ''
    update_action_text()


def operator_change(attr, old, new):
    update_input_text()
    update_action_text()


def category_change(attr, old, new):
    update_input_text()
    update_action_text()


def update_input_text():
    update_input_text_title()
    update_input_text_value()


def update_action_text():
    category_map = {0: select_institutional_roi.value,
                    1: select_physician.value,
                    2: select_physician_roi.value,
                    3: select_variation.value}

    current = {0: db.get_institutional_rois(),
               1: db.get_physicians(),
               2: db.get_physician_rois(select_physician.value),
               3: db.get_variations(select_physician.value, select_physician_roi.value)}

    in_value = category_map[category.active]

    input_text_value = clean_name(input_text.value)
    if category.active == 1:
        input_text_value = input_text_value.upper()

    if input_text_value == '' or \
            (select_physician.value == 'DEFAULT' and category.active != 0) or \
            (operator.active == 1 and input_text_value not in current[category.active]) or \
            (operator.active == 2 and input_text_value in current[category.active]) or \
            (operator.active != 0 and category.active == 3 and select_variation.value == select_physician_roi.value):
        text = "<b>No Action</b>"

    else:

        text = "<b>" + input_text.title[:-1] + " </b><i>"
        if operator.active == 0:
            text += input_text_value
        else:
            text += in_value
        text += "</i>"
        output = input_text_value

        if operator.active == 0:
            if category.active == 2:
                text += " linked to Institutional ROI <i>uncategorized</i>"
            if category.active == 3:
                text += " linked to Physician ROI <i>" + select_physician_roi.value + "</i>"

        elif operator.active == 2:
            text += " to <i>" + output + "</i>"

    div_action.text = text
    action_button.label = input_text.title[:-1]


def input_text_change(attr, old, new):
    update_action_text()


def reload_db():
    global db, category, operator

    db = DatabaseROIs()

    category.active = 0
    operator.active = 0

    input_text.value = ''

    new_options = db.get_institutional_rois()
    select_institutional_roi.options = new_options
    select_institutional_roi.value = new_options[0]

    new_options = db.get_physicians()
    if len(new_options) > 1:
        new_value = new_options[1]
    else:
        new_value = new_options[0]
    select_physician.options = new_options
    select_physician.value = new_value

    save_button_roi.button_type = 'primary'
    save_button_roi.label = 'Map Saved'


def save_db():
    db.write_to_file()
    save_button_roi.button_type = 'primary'
    save_button_roi.label = 'Map Saved'
    update_roi_map_table_source()


def update_roi_map_source_data():
    roi_map_source.data = db.get_physician_roi_visual_coordinates(select_physician.value,
                                                                  select_physician_roi.value)


function_map = {'Add Institutional ROI': add_institutional_roi,
                'Add Physician': add_physician,
                'Add Physician ROI': add_physician_roi,
                'Add Variation': add_variation,
                'Delete Institutional ROI': delete_institutional_roi,
                'Delete Physician': delete_physician,
                'Delete Physician ROI': delete_physician_roi,
                'Delete Variation': delete_variation,
                'Rename Institutional ROI': rename_institutional_roi,
                'Rename Physician': rename_physician,
                'Rename Physician ROI': rename_physician_roi,
                'Rename Variation': rename_variation}


def execute_button_click():
    function_map[input_text.title.strip(':')]()
    update_roi_map_source_data()
    update_uncategorized_variation_select()
    update_save_button_status()


def unlinked_institutional_roi_change(attr, old, new):
    if select_physician.value != 'DEFAULT':
        db.set_linked_institutional_roi(new, select_physician.value, select_physician_roi.value)
        update_action_text()
        update_roi_map_source_data()


def update_select_unlinked_institutional_roi():
    new_options = db.get_unused_institutional_rois(select_physician.value)
    new_value = db.get_institutional_roi(select_physician.value, select_physician_roi.value)
    if new_value not in new_options:
        new_options.append(new_value)
        new_options.sort()
    select_unlinked_institutional_roi.options = new_options
    select_unlinked_institutional_roi.value = new_value


def update_uncategorized_variation_change(attr, old, new):
    update_input_text()


def update_uncategorized_variation_select():
    global uncategorized_variations
    uncategorized_variations = get_uncategorized_variations(select_physician.value)
    new_options = list(uncategorized_variations)
    new_options.sort()
    old_value_index = select_uncategorized_variation.options.index(select_uncategorized_variation.value)
    select_uncategorized_variation.options = new_options
    if old_value_index < len(new_options) - 1:
        select_uncategorized_variation.value = new_options[old_value_index]
    else:
        try:
            select_uncategorized_variation.value = new_options[old_value_index - 1]
        except IndexError:
            select_uncategorized_variation.value = new_options[0]
    update_input_text()


def update_ignored_variations_select():
    new_options = list(get_ignored_variations(select_physician.value))
    new_options.sort()
    select_ignored_variation.options = new_options
    select_ignored_variation.value = new_options[0]


def get_uncategorized_variations(physician):
    global config
    if validate_sql_connection(config=config, verbose=False):
        physician = clean_name(physician).upper()
        condition = "physician_roi = 'uncategorized'"
        cursor_rtn = DVH_SQL().query('dvhs', 'roi_name, study_instance_uid', condition)
        new_uncategorized_variations = {}
        cnx = DVH_SQL()
        for row in cursor_rtn:
            variation = clean_name(str(row[0]))
            study_instance_uid = str(row[1])
            physician_db = cnx.query('plans', 'physician', "study_instance_uid = '" + study_instance_uid + "'")
            if physician_db:
                physician_db = physician_db[0][0]
            new_uncategorized_variations_keys = list(new_uncategorized_variations)
            if physician == physician_db and variation not in new_uncategorized_variations_keys:
                new_uncategorized_variations[variation] = {'roi_name': str(row[0]), 'study_instance_uid': str(row[1])}
        if new_uncategorized_variations:
            return new_uncategorized_variations
        else:
            return {' ': ''}
    else:
        return ['Could not connect to SQL']


def get_ignored_variations(physician):
    global config
    if validate_sql_connection(config=config, verbose=False):
        physician = clean_name(physician).upper()
        condition = "physician_roi = 'ignored'"
        cursor_rtn = DVH_SQL().query('dvhs', 'roi_name, study_instance_uid', condition)
        new_ignored_variations = {}
        cnx = DVH_SQL()
        for row in cursor_rtn:
            variation = clean_name(str(row[0]))
            study_instance_uid = str(row[1])
            physician_db = cnx.query('plans', 'physician', "study_instance_uid = '" + study_instance_uid + "'")[0][0]
            new_ignored_variations_keys = list(new_ignored_variations)
            if physician == physician_db and variation not in new_ignored_variations_keys:
                new_ignored_variations[variation] = {'roi_name': str(row[0]), 'study_instance_uid': str(row[1])}
        if new_ignored_variations:
            return new_ignored_variations
        else:
            return {' ': ''}
    else:
        return ['Could not connect to SQL']


def delete_uncategorized_dvh():
    if delete_uncategorized_button_roi.button_type == 'warning':
        if select_uncategorized_variation.value != ' ':
            delete_uncategorized_button_roi.button_type = 'danger'
            delete_uncategorized_button_roi.label = 'Are you sure?'
            ignore_button_roi.button_type = 'success'
            ignore_button_roi.label = 'Cancel Delete DVH'
    else:
        physician_uids = DVH_SQL().query('Plans', 'study_instance_uid', "physician = '%s'" % select_physician.value)
        physician_uids = [uid[0] for uid in physician_uids]
        uids = DVH_SQL().query('DVHs', 'study_instance_uid', "roi_name = '%s'" % select_uncategorized_variation.value)
        for uid in uids:
            if uid[0] in physician_uids:
                DVH_SQL().delete_dvh(select_uncategorized_variation.value, uid[0])
        update_uncategorized_variation_select()
        update_ignored_variations_select()
        delete_uncategorized_button_roi.button_type = 'warning'
        delete_uncategorized_button_roi.label = 'Delete DVH'
        ignore_button_roi.button_type = 'primary'
        ignore_button_roi.label = 'Ignore'


def delete_ignored_dvh():
    if delete_ignored_button_roi.button_type == 'warning':
        if select_ignored_variation.value != ' ':
            delete_ignored_button_roi.button_type = 'danger'
            delete_ignored_button_roi.label = 'Are you sure?'
            unignore_button_roi.button_type = 'success'
            unignore_button_roi.label = 'Cancel Delete DVH'
    else:
        physician_uids = DVH_SQL().query('Plans', 'study_instance_uid', "physician = '%s'" % select_physician.value)
        physician_uids = [uid[0] for uid in physician_uids]
        uids = DVH_SQL().query('DVHs', 'study_instance_uid', "roi_name = '%s'" % select_ignored_variation.value)
        for uid in uids:
            if uid[0] in physician_uids:
                DVH_SQL().delete_dvh(select_ignored_variation.value, uid[0])
        update_uncategorized_variation_select()
        update_ignored_variations_select()
        delete_ignored_button_roi.button_type = 'warning'
        delete_ignored_button_roi.label = 'Delete DVH'
        unignore_button_roi.button_type = 'primary'
        unignore_button_roi.label = 'Unignore'


def ignore_dvh():
    global config
    if ignore_button_roi.label == 'Cancel Delete DVH':
        ignore_button_roi.button_type = 'primary'
        ignore_button_roi.label = 'Ignore'
        delete_uncategorized_button_roi.button_type = 'warning'
        delete_uncategorized_button_roi.label = 'Delete DVH'
    else:
        cnx = DVH_SQL()
        if validate_sql_connection(config=config, verbose=False):
            condition = "physician_roi = 'uncategorized'"
            cursor_rtn = DVH_SQL().query('dvhs', 'roi_name, study_instance_uid', condition)
            for row in cursor_rtn:
                variation = str(row[0])
                study_instance_uid = str(row[1])
                if clean_name(variation) == select_uncategorized_variation.value:
                    cnx.update('dvhs', 'physician_roi', 'ignored', "roi_name = '" + variation +
                               "' and study_instance_uid = '" + study_instance_uid + "'")
        cnx.close()
        to_be_ignored = select_uncategorized_variation.value
        update_uncategorized_variation_select()
        update_ignored_variations_select()
        select_ignored_variation.value = to_be_ignored


def unignore_dvh():
    global config
    if unignore_button_roi.label == 'Cancel Delete DVH':
        unignore_button_roi.button_type = 'primary'
        unignore_button_roi.label = 'Ignore'
        delete_ignored_button_roi.button_type = 'warning'
        delete_ignored_button_roi.label = 'Delete DVH'
    else:
        cnx = DVH_SQL()
        if validate_sql_connection(config=config, verbose=False):
            condition = "physician_roi = 'ignored'"
            cursor_rtn = DVH_SQL().query('dvhs', 'roi_name, study_instance_uid', condition)
            for row in cursor_rtn:
                variation = str(row[0])
                study_instance_uid = str(row[1])
                if clean_name(variation) == select_ignored_variation.value:
                    cnx.update('dvhs', 'physician_roi', 'uncategorized', "roi_name = '" + variation +
                               "' and study_instance_uid = '" + study_instance_uid + "'")
        cnx.close()
        to_be_unignored = select_ignored_variation.value
        update_uncategorized_variation_select()
        update_ignored_variations_select()
        select_uncategorized_variation.value = to_be_unignored


def remap_rois(cursor_rtn, button, *physician):
    if physician:
        physician = physician[0]
    else:
        physician = False

    initial_label = button.label
    cnx = DVH_SQL()
    progress = 0
    complete = len(cursor_rtn)
    for row in cursor_rtn:
        progress += 1
        variation = str(row[0])
        study_instance_uid = str(row[1])
        current_physician = cnx.query('plans', 'physician', "study_instance_uid = '" + study_instance_uid + "'")[0][0]

        if not physician or physician == current_physician:

            new_physician_roi = db.get_physician_roi(current_physician, variation)

            if new_physician_roi == 'uncategorized':
                if clean_name(variation) in db.get_institutional_rois():
                    new_institutional_roi = clean_name(variation)
                else:
                    new_institutional_roi = 'uncategorized'
            else:
                new_institutional_roi = db.get_institutional_roi(current_physician, new_physician_roi)

            condition_str = "roi_name = '" + variation + "' and study_instance_uid = '" + study_instance_uid + "'"
            cnx.update('dvhs', 'physician_roi', new_physician_roi, condition_str)
            cnx.update('dvhs', 'institutional_roi', new_institutional_roi, condition_str)

            percent = int(float(100) * (float(progress) / float(complete)))
            button.label = "Remap progress: " + str(percent) + "%"
    button.label = initial_label

    db.write_to_file()
    update_uncategorized_variation_select()
    update_ignored_variations_select()


def update_uncategorized_rois_in_db():
    cursor_rtn = DVH_SQL().query('dvhs', 'roi_name, study_instance_uid', "physician_roi = 'uncategorized'")
    remap_rois(cursor_rtn, update_uncategorized_rois_button)


def remap_all_rois_in_db():
    cursor_rtn = DVH_SQL().query('dvhs', 'roi_name, study_instance_uid')
    remap_rois(cursor_rtn, remap_all_rois_button)


def remap_all_rois_for_selected_physician():
    cursor_rtn = DVH_SQL().query('dvhs', 'roi_name, study_instance_uid')
    remap_rois(cursor_rtn, remap_all_rois_for_selected_physician_button, select_physician.value)


def update_save_button_status():
    save_button_roi.button_type = 'success'
    save_button_roi.label = 'Map Save Needed'


def update_query_columns_ticker(attr, old, new):
    update_query_columns()


def update_query_columns():
    new_options = DVH_SQL().get_column_names(query_table.value.lower())
    # new_options.pop(new_options.index('mrn'))
    # new_options.pop(new_options.index('study_instance_uid'))
    if query_table.value.lower() == 'dvhs':
        new_options.pop(new_options.index('dvh_string'))
        new_options.pop(new_options.index('roi_coord_string'))
        new_options.pop(new_options.index('dth_string'))
    options_tuples = []
    for option in new_options:
        options_tuples.append(tuple([option, option]))
    query_columns.options = options_tuples
    query_columns.value = ['']


def update_update_db_columns_ticker(attr, old, new):
    update_update_db_column()


def update_update_db_column():
    new_options = DVH_SQL().get_column_names(update_db_table.value.lower())
    new_options.pop(new_options.index('import_time_stamp'))
    if update_db_table.value.lower() == 'dvhs':
        new_options.pop(new_options.index('dvh_string'))
        new_options.pop(new_options.index('roi_coord_string'))

    update_db_column.options = new_options
    update_db_column.value = new_options[0]


def update_query_source():

    columns = query_columns.value
    if 'mrn' not in columns:
        columns.insert(0, 'mrn')
    if 'study_instance_uid' not in columns:
        columns.insert(1, 'study_instance_uid')
    new_data = {}
    table_columns = []
    if not columns[-1]:
        columns.pop()
    for column in columns:
        new_data[column] = []
        table_columns.append(TableColumn(field=column, title=column))
    columns_str = ','.join(columns).strip()
    if query_condition.value:
        query_cursor = DVH_SQL().query(query_table.value, columns_str, query_condition.value)
    else:
        query_cursor = DVH_SQL().query(query_table.value, columns_str)

    for row in query_cursor:
        for i in range(len(columns)):
            new_data[columns[i]].append(str(row[i]))

    if new_data:
        query_source.data = new_data

        data_table_new = DataTable(source=query_source, columns=table_columns,
                                   width=int(table_slider.value), editable=True)
        db_editor_layout.children.pop()
        db_editor_layout.children.append(data_table_new)

    update_csv()


def update_db():
    if update_db_condition.value and update_db_value.value:
        update_db_button.label = 'Updating...'
        update_db_button.button_type = 'danger'
        update_value = update_db_value.value
        if update_db_column.value in {'birth_date', 'sim_study_date'}:
            update_value = update_value + "::date"
        DVH_SQL().update(update_db_table.value, update_db_column.value, update_value, update_db_condition.value)
        update_query_source()
        update_db_button.label = 'Update'
        update_db_button.button_type = 'warning'


def delete_from_db():
    if delete_from_db_value.value and delete_auth_text.value == 'delete':
        condition = delete_from_db_column.value + " = '" + delete_from_db_value.value + "'"
        DVH_SQL().delete_rows(condition)
        update_query_source()
        delete_from_db_value.value = ''
        delete_auth_text.value = ''


def change_mrn_uid():
    change_mrn_uid_button.label = 'Updating...'
    change_mrn_uid_button.button_type = 'danger'
    old = change_mrn_uid_old_value.value
    new = change_mrn_uid_new_value.value
    if old and new and old != new:
        if change_mrn_uid_column.value == 'mrn':
            DVH_SQL().change_mrn(old, new)
        elif change_mrn_uid_column.value == 'study_instance_uid':
            DVH_SQL().change_uid(old, new)
    change_mrn_uid_old_value.value = ''
    change_mrn_uid_new_value.value = ''
    change_mrn_uid_button.label = 'Rename'
    change_mrn_uid_button.button_type = 'warning'
    update_query_source()


def delete_auth_text_ticker(attr, old, new):
    if new == 'delete':
        delete_from_db_button.button_type = 'danger'
    else:
        delete_from_db_button.button_type = 'warning'


def import_inbox():
    if import_inbox_button.label in {'Cancel'}:
        rebuild_db_button.label = 'Rebuild database'
        rebuild_db_button.button_type = 'warning'
    else:
        import_inbox_button.button_type = 'warning'
        import_inbox_button.label = 'Importing...'
        if 0 in import_inbox_force.active:
            force_update = True
        else:
            force_update = False

        if 2 in import_inbox_force.active:
            move_files = True
        else:
            move_files = False

        if 1 in import_inbox_force.active:
            import_latest_only = True
        else:
            import_latest_only = False
        dicom_to_sql(force_update=force_update, import_latest_only=import_latest_only, move_files=move_files)
    import_inbox_button.button_type = 'success'
    import_inbox_button.label = 'Import all from inbox'

    # initial_condition = calculate_condition.value
    # calculate_condition.value = 'dist_to_ptv_min is NULL'
    # calculate_ptv_distances()
    # calculate_condition.value = 'ptv_overlap is NULL'
    # calculate_ptv_overlap()
    # calculate_condition.value = initial_condition


def rebuild_db_button_click():
    if rebuild_db_button.button_type in {'warning'}:
        rebuild_db_button.label = 'Are you sure?'
        rebuild_db_button.button_type = 'danger'
        import_inbox_button.button_type = 'success'
        import_inbox_button.label = 'Cancel'

    else:
        rebuild_db_button.label = 'Rebuilding...'
        rebuild_db_button.button_type = 'danger'
        import_inbox_button.button_type = 'success'
        import_inbox_button.label = 'Import all from inbox'
        rebuild_database(directories['imported'])
        rebuild_db_button.label = 'Rebuild database'
        rebuild_db_button.button_type = 'warning'


def backup_db():
    backup_db_button.button_type = 'warning'
    backup_db_button.label = 'Backing up...'

    script_dir = os.path.dirname(__file__)
    abs_path = os.path.join(script_dir, "backups")
    if not os.path.isdir(abs_path):
        os.mkdir(abs_path)

    time_id = str(datetime.now()).split('.')[0].replace(':', '-').replace(' ', '_')
    new_file = config['dbname'] + '_' + config['host'] + '_' + config['port'] +\
               '_' + time_id +\
               '.sql'
    abs_file_path = os.path.join(abs_path, new_file)

    if os.path.isfile('/this_is_running_in_docker'):
        os.system("pg_dump -U %s -h %s %s > %s" % (config['user'], config['host'], config['dbname'], abs_file_path))
    else:
        os.system("pg_dumpall >" + abs_file_path)

    update_backup_select(backup_location.value)

    backup_db_button.button_type = 'success'
    backup_db_button.label = 'Backup'


def restore_db():
    restore_db_button.label = 'Restoring...'
    restore_db_button.button_type = 'warning'

    DVH_SQL().drop_tables()

    script_dir = os.path.dirname(__file__)
    rel_path = os.path.join("backups", backup_select.value)
    abs_file_path = os.path.join(script_dir, rel_path)

    back_up_command = "psql " + config['dbname'] + " < " + abs_file_path
    os.system(back_up_command)

    restore_db_button.label = 'Restore'
    restore_db_button.button_type = 'primary'


def backup_pref():
    backup_pref_button.button_type = 'warning'
    backup_pref_button.label = 'Backing up...'

    script_dir = os.path.dirname(__file__)
    backup_path = os.path.join(script_dir, "backups")
    pref_path = os.path.join(script_dir, 'preferences')
    if not os.path.isdir(backup_path):
        os.mkdir(backup_path)

    time_id = str(datetime.now()).split('.')[0].replace(':', '-').replace(' ', '_')
    backup_path_pref = os.path.join(backup_path, "preferences_" + time_id)
    if not os.path.isdir(backup_path_pref):
        os.mkdir(backup_path_pref)

    files_to_backup = [f for f in os.listdir(pref_path) if os.path.isfile(os.path.join(pref_path, f))]
    for f in files_to_backup:
        copyfile(os.path.join(pref_path, f), os.path.join(backup_path_pref, f))

    update_backup_select(backup_location.value)

    backup_pref_button.button_type = 'success'
    backup_pref_button.label = 'Backup'


def update_backup_select(abs_path, *new_index):

    if not os.path.isdir(abs_path):
        try:
            os.mkdir(abs_path)
        except OSError:
            backup_location.value = 'Invalid Path'
            time.sleep(2.5)
            backup_location.value = '/'

    # SQL Backups
    backups = [f for f in os.listdir(abs_path) if os.path.isfile(os.path.join(abs_path, f)) and '.sql' in f]
    if not backups:
        backups = ['']
    backups.sort(reverse=True)
    backup_select.options = backups
    if new_index:
        backup_select.value = backups[new_index[0]]
    else:
        backup_select.value = backups[0]

    # Preferences backups
    backups = [d for d in os.listdir(abs_path) if os.path.isdir(os.path.join(abs_path, d)) and d.startswith('preferences')]
    if not backups:
        backups = ['']
    backups.sort(reverse=True)
    backup_pref_select.options = backups


def delete_backup():
    old_index = backup_select.options.index(backup_select.value)

    script_dir = os.path.dirname(__file__)
    abs_path = os.path.join(script_dir, 'backups')
    abs_file = os.path.join(abs_path, backup_select.value)

    if os.path.isfile(abs_file):
        os.remove(abs_file)
        if old_index < len(backup_select.options) - 1:
            new_index = old_index
        else:
            new_index = len(backup_select.options) - 2
        update_backup_select(backup_location.value, new_index)


def delete_backup_pref():
    delete_backup_button_pref.label = 'Restoring...'
    delete_backup_button_pref.button_type = 'warning'

    script_dir = os.path.dirname(__file__)
    src_path = os.path.join(script_dir, 'backups', backup_pref_select.value)

    for f in os.listdir(src_path):
        os.remove(f)
    os.rmdir(src_path)

    update_backup_select(backup_location.value)

    delete_backup_button_pref.label = 'Restore'
    delete_backup_button_pref.button_type = 'primary'


def restore_preferences():
    restore_pref_button.label = 'Restoring...'
    restore_pref_button.button_type = 'warning'

    script_dir = os.path.dirname(__file__)
    backup_path = os.path.join(script_dir, 'backups')
    dest_path = os.path.join(script_dir, 'preferences')
    src_path = os.path.join(backup_path, backup_pref_select.value)

    for f in os.listdir(dest_path):
        os.remove(f)

    files_to_restore = [f for f in os.listdir(src_path) if os.path.isfile(os.path.join(src_path, f))]
    for f in files_to_restore:
        copyfile(os.path.join(src_path, f), os.path.join(dest_path, f))

    update_backup_select(backup_location.value)

    restore_pref_button.label = 'Restore'
    restore_pref_button.button_type = 'primary'


def update_baseline_source():
    baseline_layout.children.pop()
    columns = ['mrn', 'sim_study_date', 'physician', 'rx_dose', 'fxs', 'tx_modality', 'tx_site',
               'study_instance_uid', 'import_time_stamp', 'baseline']
    new_data = {}
    table_columns = []
    for column in columns:
        new_data[column] = []
        table_columns.append(TableColumn(field=column, title=column))
    columns_str = ','.join(columns).strip()
    if baseline_condition.value:
        query_cursor = DVH_SQL().query('Plans', columns_str, baseline_condition.value)
    else:
        query_cursor = DVH_SQL().query('Plans', columns_str)

    for row in query_cursor:
        for i in range(len(columns)):
            new_data[columns[i]].append(str(row[i]))

    baseline_source.data = new_data

    baseline_table_new = DataTable(source=baseline_source, columns=table_columns, width=baseline_table_slider.value, editable=True)
    baseline_layout.children.append(baseline_table_new)

    update_baseline_mrns()


def update_baseline_mrns():
    if len(baseline_source.data['mrn']) == 0:
        options = ['']
    else:
        options = []
        for i in range(len(baseline_source.data['mrn'])):
            options.append(baseline_source.data['mrn'][i])
        options.sort()

    baseline_mrn_select.options = options
    baseline_mrn_select.value = options[0]

    update_baseline_study_dates()


def update_baseline_study_dates():

    if len(baseline_source.data['mrn']) == 0:
        options = ['']
    else:
        study_dates = []

        for i in range(len(baseline_source.data['mrn'])):
            if baseline_source.data['mrn'][i] == baseline_mrn_select.value:
                study_dates.append(baseline_source.data['sim_study_date'][i])

        options = []
        for i in range(len(study_dates)):
            options.append(study_dates[i])
        options.sort()

    baseline_study_date_select.options = options
    baseline_study_date_select.value = options[0]

    update_baseline_uid()


def update_baseline_uid():
    if len(baseline_source.data['mrn']) == 0:
        options = ['']
    else:
        uids = []

        for i in range(len(baseline_source.data['mrn'])):
            if baseline_source.data['mrn'][i] == baseline_mrn_select.value:
                if baseline_source.data['sim_study_date'][i] == baseline_study_date_select.value:
                    uids.append(baseline_source.data['study_instance_uid'][i])
        options = uids
        options.sort()

    baseline_uid_select.options = options
    baseline_uid_select.value = options[0]

    update_baseline_status_select()


def update_baseline_status_select():
    if len(baseline_source.data['mrn']) == 0:
        baseline_status_select.options = ['']
        baseline_status_select.value = ''
    else:
        index = baseline_source.data['study_instance_uid'].index(baseline_uid_select.value)
        baseline_status_select.options = ['True', 'False']
        baseline_status_select.value = baseline_source.data['baseline'][index]


def update_baseline_mrn_ticker(attr, old, new):
    update_baseline_study_dates()


def update_baseline_study_date_ticker(attr, old, new):
    update_baseline_uid()


def update_baseline_uid_ticker(attr, old, new):
    update_baseline_status_select()


def update_baseline_status_ticker(attr, old, new):
    uid = baseline_uid_select.value
    current_baseline = DVH_SQL().query('Plans', 'baseline', "study_instance_uid = '" + uid + "'")[0][0]

    if new not in {str(current_baseline), ''}:
        if new == 'True':
            baseline = 1
        else:
            baseline = 0

        DVH_SQL().update('Plans', 'baseline', baseline, "study_instance_uid = '" + baseline_uid_select.value + "'")
        update_baseline_source()


def source_selection_ticker(attr, old, new):
    index = baseline_source.selected.indices[0]
    mrn = baseline_source.data['mrn'][index]
    date = baseline_source.data['sim_study_date'][index]
    uid = baseline_source.data['study_instance_uid'][index]
    baseline_mrn_select.value = mrn
    baseline_study_date_select.value = date
    baseline_uid_select.value = uid


def update_all_min_distances_in_db(*condition):
    if condition:
        condition = " AND (" + condition[0] + ")"
    else:
        condition = ''
    condition = "(LOWER(roi_type) IN ('organ', 'ctv', 'gtv') AND (" \
                "LOWER(roi_name) NOT IN ('external', 'skin') OR " \
                "LOWER(physician_roi) NOT IN ('uncategorized', 'ignored', 'external', 'skin')))" + condition
    rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi', condition)
    counter = 0.
    total_rois = float(len(rois))
    for roi in rois:
        calculate_exec_button.label = str(int((counter / total_rois) * 100)) + '%'
        counter += 1.
        if roi[1].lower() not in {'external', 'skin'} and \
                        roi[2].lower() not in {'uncategorized', 'ignored', 'external', 'skin'}:
            print('updating dist to ptv:', roi[1], sep=' ')
            update_min_distances_in_db(roi[0], roi[1])
        else:
            print('skipping dist to ptv:', roi[1], sep=' ')


def update_all_tv_overlaps_in_db(*condition):
    if condition:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi', condition[0])
    else:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi')
    counter = 0.
    total_rois = float(len(rois))
    for roi in rois:
        calculate_exec_button.label = str(int((counter / total_rois) * 100)) + '%'
        counter += 1.
        print('updating ptv_overlap:', roi[1], sep=' ')
        update_treatment_volume_overlap_in_db(roi[0], roi[1])


def update_all_centroids_in_db(*condition):
    if condition:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi', condition[0])
    else:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi')
    counter = 0.
    total_rois = float(len(rois))
    for roi in rois:
        calculate_exec_button.label = str(int((counter / total_rois) * 100)) + '%'
        counter += 1.
        print('updating centroid:', roi[1], sep=' ')
        update_centroid_in_db(roi[0], roi[1])


def update_all_spreads_in_db(*condition):
    if condition:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi', condition[0])
    else:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi')
    counter = 0.
    total_rois = float(len(rois))
    for roi in rois:
        calculate_exec_button.label = str(int((counter / total_rois) * 100)) + '%'
        counter += 1.
        print('updating spread:', roi[1], sep=' ')
        update_spread_in_db(roi[0], roi[1])


def update_all_cross_sections_in_db(*condition):
    if condition:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi', condition[0])
    else:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi')
    counter = 0.
    total_rois = float(len(rois))
    for roi in rois:
        calculate_exec_button.label = str(int((counter / total_rois) * 100)) + '%'
        counter += 1.
        print('updating cross-section:', roi[1], sep=' ')
        update_cross_section_in_db(roi[0], roi[1])


def update_all_dist_to_ptv_centoids_in_db(*condition):

    if condition:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi', condition[0])
    else:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi')
    counter = 0.
    total_rois = float(len(rois))
    for roi in rois:
        calculate_exec_button.label = str(int((counter / total_rois) * 100)) + '%'
        counter += 1.
        print('updating min_dist_to_ptv_centroid:', roi[1], sep=' ')
        update_dist_to_ptv_centroids_in_db(roi[0], roi[1])


def update_all_except_age_in_db():

    for f in calculate_select.options:
        if f not in {'Patient Ages', 'Default Post-Import'}:
            calculate_select.value = f
            calculate_exec()


def update_default_post_import():

    for f in ['PTV Distances', 'PTV Overlap', 'OAR-PTV Centroid Dist']:
        calculate_select.value = f
        calculate_exec()
    calculate_select.value = 'Default Post-Import'


# Calculates volumes using Shapely, not dicompyler
# This function is not in the GUI
def recalculate_roi_volumes(*condition):
    if condition:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi', condition[0])
    else:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi')
    counter = 0.
    total_rois = float(len(rois))
    for roi in rois:
        counter += 1.
        print('updating volume:', roi[1], int(100. * counter / total_rois), sep=' ')
        update_volumes_in_db(roi[0], roi[1])


# Calculates surface area using Shapely
# This function is not in the GUI
def recalculate_surface_areas(*condition):
    if condition:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi', condition[0])
    else:
        rois = DVH_SQL().query('dvhs', 'study_instance_uid, roi_name, physician_roi')
    counter = 0.
    total_rois = float(len(rois))
    for roi in rois:
        counter += 1.
        print('updating surface area:', roi[1], int(100. * counter / total_rois), sep=' ')
        update_surface_area_in_db(roi[0], roi[1])


def auth_button_click():
    global ACCESS_GRANTED

    if not ACCESS_GRANTED:
        ACCESS_GRANTED = auth.check_credentials(auth_user.value, auth_pass.value, 'admin')
        if ACCESS_GRANTED:
            auth_button.label = 'Access Granted'
            auth_button.button_type = 'success'
            curdoc().clear()
            curdoc().add_root(tabs)
        else:
            auth_button.label = 'Failed'
            auth_button.button_type = 'danger'
            time.sleep(3)
            auth_button.label = 'Authenticate'
            auth_button.button_type = 'warning'


def reimport_mrn_ticker(attr, old, new):
    new_options = DVH_SQL().get_unique_values('Plans', 'sim_study_date', "mrn = '%s'" % new)
    if not new_options:
        new_options = ['MRN not found']
    reimport_study_date_select.options = new_options
    reimport_study_date_select.value = new_options[0]


def reimport_study_date_ticker(attr, old, new):
    if new != 'MRN not found':
        if new == 'None':
            new_options = DVH_SQL().get_unique_values('Plans',
                                                      'study_instance_uid',
                                                      "mrn = '%s'" %
                                                      reimport_mrn_text.value)
        else:
            new_options = DVH_SQL().get_unique_values('Plans',
                                                      'study_instance_uid',
                                                      "mrn = '%s' and sim_study_date = '%s'" %
                                                      (reimport_mrn_text.value, new))
    else:
        new_options = ['Study Date not found']

    reimport_uid_select.options = new_options
    reimport_uid_select.value = new_options[0]


def reimport_button_click():
    dicom_directory = DVH_SQL().query('DICOM_Files',
                                      "folder_path",
                                      "study_instance_uid = '%s'" % reimport_uid_select.value)[0][0]
    if os.path.isdir(dicom_directory):
        if not os.listdir(dicom_directory):
            print("WARNING: %s is empty." % dicom_directory)
            print("Aborting DICOM reimport.")
        else:
            reimport_button.label = "Updating..."
            reimport_button.button_type = 'danger'
            if reimport_old_data_select.value == "Delete from DB":
                DVH_SQL().delete_rows("study_instance_uid = '%s'" % reimport_uid_select.value,
                                      ignore_table=['DICOM_Files'])

            dicom_to_sql(start_path=dicom_directory, force_update=True,
                         move_files=False, update_dicom_catalogue_table=False)
            reimport_button.label = "Reimport"
            reimport_button.button_type = 'warning'
    else:
        print("WARNING: %s does not exist" % dicom_directory)
        print("Aborting DICOM reimport.")


options_map = {'Default': os.path.join(os.path.dirname(__file__), 'backups'),
               'Root': '/',
               'Home': os.path.expanduser('~'),
               'Custom': ''}


def backup_location_select_ticker(attr, old, new):
    if new != 'Custom':
        backup_location.value = options_map[new]


def backup_location_ticker(attr, old, new):
    if new not in listvalues(options_map):
        backup_location_select.value = 'Custom'
    update_backup_select(new)


def calculate_exec():
    calc_map = {'PTV Distances': update_all_min_distances_in_db,
                'PTV Overlap': update_all_tv_overlaps_in_db,
                'Patient Ages': recalculate_ages,
                'ROI Centroid': update_all_centroids_in_db,
                'ROI Spread': update_all_spreads_in_db,
                'ROI Cross-Section': update_all_cross_sections_in_db,
                'OAR-PTV Centroid Dist': update_all_dist_to_ptv_centoids_in_db,
                'All (except age)': update_all_except_age_in_db,
                'Default Post-Import': update_default_post_import}

    if calculate_select.value not in {'All (except age)', 'Default Post-Import'}:

        start_time = datetime.now()
        print(str(start_time), 'Beginning %s calculations' % calculate_condition.value, sep=' ')

        calculate_exec_button.label = 'Calculating...'
        calculate_exec_button.button_type = 'warning'

        if calculate_condition.value:
            calc_map[calculate_select.value](calculate_condition.value)
        else:
            calc_map[calculate_select.value]()

        update_query_source()

        calculate_exec_button.label = 'Perform Calc'
        calculate_exec_button.button_type = 'primary'

        end_time = datetime.now()
        print(str(end_time), 'Calculations complete', sep=' ')

        total_time = end_time - start_time
        seconds = total_time.seconds
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h:
            print("These calculations took %dhrs %02dmin %02dsec to complete" % (h, m, s))
        elif m:
            print("These calculations took %02dmin %02dsec to complete" % (m, s))
        else:
            print("These calculations took %02dsec to complete" % s)
    else:
        if calculate_condition.value:
            calc_map[calculate_select.value](calculate_condition.value)
        else:
            calc_map[calculate_select.value]()


def update_csv():
    src_data = [query_source.data]
    src_names = ['Queried Data']
    columns = list(src_data[0])

    mrn_index, uid_index = None, None
    for i, c in enumerate(columns):
        if c == 'mrn':
            mrn_index = i
        if c == 'study_instance_uid':
            uid_index = i

    if uid_index is not None:
        columns.pop(uid_index)
        columns.insert(0, 'study_instance_uid')
    if mrn_index is not None:
        columns.pop(mrn_index)
        columns.insert(0, 'mrn')

    csv_text = get_csv(src_data, src_names, columns)

    query_data_csv.data = {'text': [csv_text]}


def update_roi_map_table_source():
    phys_roi = db.get_physician_rois(select_physician.value)
    inst_roi = [db.get_institutional_roi(select_physician.value, roi) for roi in phys_roi]
    vari_roi = [', '.join(db.get_variations(select_physician.value, roi)) for roi in phys_roi]
    roi_map_table_source.data = {'institutional_roi': inst_roi,
                                 'physician_roi': phys_roi,
                                 'variation_roi': vari_roi}
    div_roi_map_table.text = "<b>Currently Saved ROI Map for %s" % select_physician.value


######################################################
# Layout objects
######################################################

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Custom authorization
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
auth_user = TextInput(value='', title='User Name:', width=150)
auth_pass = PasswordInput(value='', title='Password:', width=150)
auth_button = Button(label="Authenticate", button_type="warning", width=100)
auth_button.on_click(auth_button_click)
auth_div = Div(text="<b>DVH Analytics Admin</b>", width=600)
layout_login = column(auth_div,
                      row(auth_user, Spacer(width=50), auth_pass, Spacer(width=50), auth_button))


# !!!!!!!!!!!!!!!!!!!!!!!
# ROI Name Manger objects
# !!!!!!!!!!!!!!!!!!!!!!!
div_warning = Div(text="<b>WARNING:</b> Buttons in orange cannot be easily undone.", width=600)

# Selectors
roi_options = db.get_institutional_rois()
select_institutional_roi = Select(value=roi_options[0],
                                  options=roi_options,
                                  width=300,
                                  title='All Institutional ROIs')

physician_options = db.get_physicians()
if len(physician_options) > 1:
    value = physician_options[1]
else:
    value = physician_options[0]
select_physician = Select(value=value,
                          options=physician_options,
                          width=300,
                          title='Physician')

phys_roi_options = db.get_physician_rois(select_physician.value)
select_physician_roi = Select(value=phys_roi_options[0],
                              options=phys_roi_options,
                              width=300,
                              title='Physician ROIs')

variations_options = db.get_variations(select_physician.value, select_physician_roi.value)
select_variation = Select(value=variations_options[0],
                          options=variations_options,
                          width=300,
                          title='Variations')

unused_roi_options = db.get_unused_institutional_rois(select_physician.value)
value = db.get_institutional_roi(select_physician.value, select_physician_roi.value)
if value not in unused_roi_options:
    unused_roi_options.append(value)
    unused_roi_options.sort()
select_unlinked_institutional_roi = Select(value=value,
                                           options=unused_roi_options,
                                           width=300,
                                           title='Linked Institutional ROI')
uncategorized_variations = get_uncategorized_variations(select_physician.value)
try:
    uncat_var_options = list(uncategorized_variations)
except:
    uncat_var_options = ['']
uncat_var_options.sort()
select_uncategorized_variation = Select(value=uncat_var_options[0],
                                        options=uncat_var_options,
                                        width=300,
                                        title='Uncategorized Variations')
ignored_variations = get_ignored_variations(select_physician.value)
try:
    ignored_var_options = list(ignored_variations)
except:
    ignored_var_options = ['']
if not ignored_var_options:
    ignored_var_options = ['']
else:
    ignored_var_options.sort()
select_ignored_variation = Select(value=ignored_var_options[0],
                                  options=ignored_var_options,
                                  width=300,
                                  title='Ignored Variations')

div_horizontal_bar1 = Div(text="<hr>", width=900)
div_horizontal_bar2 = Div(text="<hr>", width=900)

div_action = Div(text="<b>No Action</b>", width=600)

input_text = TextInput(value='',
                       title='Add Institutional ROI:',
                       width=300)

# RadioButtonGroups
category = RadioButtonGroup(labels=categories,
                            active=0,
                            width=400)
operator = RadioButtonGroup(labels=operators,
                            active=0,
                            width=200)

# Ticker calls
select_institutional_roi.on_change('value', select_institutional_roi_change)
select_physician.on_change('value', select_physician_change)
select_physician_roi.on_change('value', select_physician_roi_change)
select_variation.on_change('value', select_variation_change)
category.on_change('active', category_change)
operator.on_change('active', operator_change)
input_text.on_change('value', input_text_change)
select_unlinked_institutional_roi.on_change('value', unlinked_institutional_roi_change)
select_uncategorized_variation.on_change('value', update_uncategorized_variation_change)

# Button objects
action_button = Button(label='Add Institutional ROI', button_type='primary', width=200)
reload_button_roi = Button(label='Reload Map', button_type='primary', width=300)
save_button_roi = Button(label='Map Saved', button_type='primary', width=300)
ignore_button_roi = Button(label='Ignore', button_type='primary', width=150)
delete_uncategorized_button_roi = Button(label='Delete DVH', button_type='warning', width=150)
unignore_button_roi = Button(label='UnIgnore', button_type='primary', width=150)
delete_ignored_button_roi = Button(label='Delete DVH', button_type='warning', width=150)
update_uncategorized_rois_button = Button(label='Update Uncategorized ROIs in DB', button_type='warning', width=300)
remap_all_rois_for_selected_physician_button = Button(label='Remap all ROIs for Physician', button_type='warning', width=300)
remap_all_rois_button = Button(label='Remap all ROIs in DB', button_type='warning', width=300)

# Button calls
action_button.on_click(execute_button_click)
reload_button_roi.on_click(reload_db)
save_button_roi.on_click(save_db)
delete_uncategorized_button_roi.on_click(delete_uncategorized_dvh)
ignore_button_roi.on_click(ignore_dvh)
delete_ignored_button_roi.on_click(delete_ignored_dvh)
unignore_button_roi.on_click(unignore_dvh)
update_uncategorized_rois_button.on_click(update_uncategorized_rois_in_db)
remap_all_rois_for_selected_physician_button.on_click(remap_all_rois_for_selected_physician)
remap_all_rois_button.on_click(remap_all_rois_in_db)

# Plot
roi_map_plot = figure(plot_width=1000, plot_height=500,
                      x_range=["Institutional ROI", "Physician ROI", "Variations"],
                      x_axis_location="above",
                      title="(Linked by Physician and Physician ROI dropdowns)",
                      tools="pan, ywheel_zoom",
                      logo=None)
roi_map_plot.toolbar.active_scroll = "auto"
roi_map_plot.title.align = 'center'
roi_map_plot.title.text_font_style = "italic"
roi_map_plot.xaxis.axis_line_color = None
roi_map_plot.xaxis.major_tick_line_color = None
roi_map_plot.xaxis.minor_tick_line_color = None
roi_map_plot.xaxis.major_label_text_font_size = "15pt"
roi_map_plot.xgrid.grid_line_color = None
roi_map_plot.ygrid.grid_line_color = None
roi_map_plot.yaxis.visible = False
roi_map_plot.outline_line_color = None
roi_map_plot.y_range = Range1d(-5, 5)

roi_map_source = ColumnDataSource(data={'name': [], 'x': [], 'y': [], 'x0': [], 'y0': [], 'x1': [], 'y1': []})
roi_map_plot.circle("x", "y", size=12, source=roi_map_source, line_color="black", fill_alpha=0.8)
labels = LabelSet(x="x", y="y", text="name", y_offset=8,
                  text_font_size="15pt", text_color="#555555",
                  source=roi_map_source, text_align='center')
roi_map_plot.add_layout(labels)
roi_map_plot.segment(x0='x0', y0='y0', x1='x1', y1='y1', source=roi_map_source, alpha=0.5)
update_roi_map_source_data()
div_roi_map_table = Div(text='')
update_roi_map_table_source()

columns = [TableColumn(field="institutional_roi", title="Institutional", width=150),
           TableColumn(field="physician_roi", title="Physician", width=150),
           TableColumn(field="variation_roi", title="Variations", width=500)]
roi_map_table = DataTable(source=roi_map_table_source, columns=columns, index_position=None, width=1000, editable=True)

roi_layout = layout([[select_institutional_roi],
                     [div_horizontal_bar1],
                     [select_physician],
                     [select_physician_roi, select_variation, select_unlinked_institutional_roi],
                     [select_uncategorized_variation, select_ignored_variation],
                     [ignore_button_roi, delete_uncategorized_button_roi, unignore_button_roi,
                      delete_ignored_button_roi],
                     [reload_button_roi, save_button_roi],
                     [update_uncategorized_rois_button, remap_all_rois_for_selected_physician_button, remap_all_rois_button],
                     [div_warning],
                     [div_horizontal_bar2],
                     [input_text, operator, category],
                     [div_action],
                     [action_button],
                     [roi_map_plot],
                     [div_roi_map_table],
                     [roi_map_table],
                     [Spacer(width=1000, height=100)]])

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Database Editor Objects
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import_inbox_button = Button(label='Import all from inbox', button_type='success', width=200)
import_inbox_button.on_click(import_inbox)
import_inbox_force = CheckboxGroup(labels=['Force Update', 'Import Latest Only', 'Move Files'], active=[1, 2])
rebuild_db_button = Button(label='Rebuild database', button_type='warning', width=200)
rebuild_db_button.on_click(rebuild_db_button_click)

query_title = Div(text="<b>Query Database</b>", width=1000)
query_table = Select(value='DVHs', options=['DVHs', 'Plans', 'Rxs', 'Beams', 'DICOM_Files'], width=200, title='Table')
query_columns = MultiSelect(title="Columns (Ctrl or Shift Click enabled)", width=250, options=[tuple(['', ''])])
query_condition = TextInput(value='', title="Condition", width=300)
query_button = Button(label='Query', button_type='primary', width=100)
table_slider = Slider(start=300, end=2000, value=1000, step=10, title="Table Width")

query_table.on_change('value', update_query_columns_ticker)
query_button.on_click(update_query_source)

update_db_title = Div(text="<b>Update Database</b>", width=1000)
update_db_table = Select(value='DVHs', options=['DVHs', 'Plans', 'Rxs', 'Beams'], width=200, height=100, title='Table')
update_db_column = Select(value='', options=[''], width=250, title='Column')
update_db_value = TextInput(value='', title="Value", width=300)
update_db_condition = TextInput(value='', title="Condition", width=300)
update_db_button = Button(label='Update DB', button_type='warning', width=100)

update_db_table.on_change('value', update_update_db_columns_ticker)
update_db_button.on_click(update_db)

update_query_columns()
update_update_db_column()

reimport_title = Div(text="<b>Reimport from DICOM</b>", width=1025)
reimport_mrn_text = TextInput(value='', width=200, title='MRN')
reimport_study_date_select = Select(value='', options=[''], width=200, height=100, title='Sim Study Date')
reimport_uid_select = Select(value='', options=[''], width=425, height=100, title='Study Instance UID')
reimport_old_data_select = Select(value='Delete from DB', options=['Delete from DB', 'Keep in DB'], width=150,
                                  height=100, title='Current Data')
reimport_button = Button(label='Reimport', button_type='warning', width=100)

reimport_mrn_text.on_change('value', reimport_mrn_ticker)
reimport_study_date_select.on_change('value', reimport_study_date_ticker)
reimport_button.on_click(reimport_button_click)

query_data_table = DataTable(source=query_source, columns=[], width=1000)

delete_from_db_title = Div(text="<b>Delete all data with mrn or study_instance_uid</b>", width=1000)
delete_from_db_column = Select(value='mrn', options=['mrn', 'study_instance_uid'], width=200, height=100,
                               title='Patient Identifier')
delete_from_db_value = TextInput(value='', title="Value (required)", width=300)
delete_from_db_button = Button(label='Delete', button_type='warning', width=100)
delete_auth_text = TextInput(value='', title="Type 'delete' here to authorize", width=300)
delete_auth_text.on_change('value', delete_auth_text_ticker)
delete_from_db_button.on_click(delete_from_db)

change_mrn_uid_title = Div(text="<b>Change mrn or study_instance_uid in all tables</b>", width=1000)
change_mrn_uid_column = Select(value='mrn', options=['mrn', 'study_instance_uid'], width=200, height=100,
                               title='Patient Identifier')
change_mrn_uid_old_value = TextInput(value='', title="Old", width=300)
change_mrn_uid_new_value = TextInput(value='', title="New", width=300)
change_mrn_uid_button = Button(label='Rename', button_type='warning', width=100)
change_mrn_uid_button.on_click(change_mrn_uid)

calculations_title = Div(text="<b>Post Import Calculations</b>", width=1000)
calculate_condition = TextInput(value='', title="Condition", width=300)
calculate_options = ['Default Post-Import', 'PTV Distances', 'PTV Overlap', 'ROI Centroid',
                     'ROI Spread', 'ROI Cross-Section', 'OAR-PTV Centroid Dist', 'All (except age)', 'Patient Ages']
calculate_select = Select(value=calculate_options[0], options=calculate_options, title='Calculate:')
calculate_exec_button = Button(label='Perform Calc', button_type='primary', width=150)
calculate_exec_button.on_click(calculate_exec)

download = Button(label="Download Table", button_type="default", width=150)
download.callback = CustomJS(args=dict(source=query_data_csv),
                             code=open(join(dirname(__file__), "download_new.js")).read())

db_editor_layout = layout([[import_inbox_button, rebuild_db_button],
                           [import_inbox_force],
                           [query_title],
                           [query_table, query_columns, query_condition, table_slider, query_button],
                           [update_db_title],
                           [update_db_table, update_db_column, update_db_condition, update_db_value,
                            update_db_button],
                           [reimport_title],
                           [reimport_mrn_text, Spacer(width=10), reimport_study_date_select, reimport_uid_select,
                            reimport_old_data_select, Spacer(width=10), reimport_button],
                           [delete_from_db_title],
                           [delete_from_db_column, delete_from_db_value, delete_auth_text, delete_from_db_button],
                           [change_mrn_uid_title],
                           [change_mrn_uid_column, change_mrn_uid_old_value,
                            change_mrn_uid_new_value, change_mrn_uid_button],
                           [calculations_title],
                           [calculate_condition, calculate_select, calculate_exec_button],
                           [download],
                           [query_data_table]])

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Baseline Objects
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
baseline_title = Div(text="<b>Query Database</b>", width=1000)
baseline_condition = TextInput(value='', title="Condition", width=625)
baseline_query_button = Button(label='Query', button_type='primary', width=100)
baseline_table_slider = Slider(start=300, end=2000, value=1025, step=10, title="Table Width")

baseline_query_button.on_click(update_baseline_source)

baseline_title_update = Div(text="<b>Update Database</b>", width=1025)
baseline_status_select = Select(value='', options=[''], width=200, height=100, title='Baseline Status')
baseline_study_date_select = Select(value='', options=[''], width=200, height=100, title='Sim Study Date')
baseline_uid_select = Select(value='', options=[''], width=425, height=100, title='Study Instance UID')
baseline_mrn_select = Select(value='', options=[''], width=200, height=100, title='MRN')

baseline_mrn_select.on_change('value', update_baseline_mrn_ticker)
baseline_study_date_select.on_change('value', update_baseline_study_date_ticker)
baseline_uid_select.on_change('value', update_baseline_uid_ticker)
baseline_status_select.on_change('value', update_baseline_status_ticker)

baseline_table = DataTable(source=baseline_source, columns=[], width=1025)

baseline_source.on_change('selected', source_selection_ticker)

baseline_layout = layout([[baseline_title],
                          [baseline_condition, baseline_table_slider, baseline_query_button],
                          [baseline_title_update],
                          [baseline_mrn_select, baseline_study_date_select, baseline_uid_select, baseline_status_select],
                          [baseline_table]])

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Backup utility
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
backup_select = Select(value='', options=[''], title="Available SQL Backups", width=450)
delete_backup_button = Button(label='Delete', button_type='warning', width=100)
restore_db_button = Button(label='Restore', button_type='primary', width=100)
backup_db_button = Button(label='Backup', button_type='success', width=100)
backup_pref_select = Select(value='', options=[''], title="Available Preferences Backups", width=450)
delete_backup_button_pref = Button(label='Delete', button_type='warning', width=100)
restore_pref_button = Button(label='Restore', button_type='primary', width=100)
backup_pref_button = Button(label='Backup', button_type='success', width=100)
backup_options = ['Default', 'Root', 'Home', 'Custom']
backup_location_select = Select(value=backup_options[0], options=backup_options, title="Common Locations")
backup_location = TextInput(value=options_map['Default'], title='Backup Directory:', width=500)
warning_div = Div(text="<b>WARNING for Non-Docker Users:</b> Restore requires your OS user name to be both a"
                       " PostgreSQL super user and have ALL PRIVILEGES WITH GRANT OPTIONS.  Do NOT attempt otherwise."
                       " It's possible you have multiple PostgreSQL servers installed, so be sure your backup"
                       " file isn't empty.  Validate by typing 'psql' in a terminal/command prompt, then"
                       " <i>SELECT * FROM pg_settings WHERE name = 'port';</i> "
                       " The resulting port should match the port below"
                       " (i.e., make sure you're backing up the correct database).", width=650)
host_div = Div(text="<b>Host</b>: %s" % config['host'])
port_div = Div(text="<b>Port</b>: %s" % config['port'])
db_div = Div(text="<b>Database</b>: %s" % config['dbname'])

backup_location_select.on_change('value', backup_location_select_ticker)
backup_location.on_change('value', backup_location_ticker)

update_backup_select(backup_location.value)

delete_backup_button.on_click(delete_backup)
backup_db_button.on_click(backup_db)
restore_db_button.on_click(restore_db)

backup_pref_button.on_click(backup_pref)

backup_layout = layout([[backup_select, delete_backup_button, restore_db_button, backup_db_button],
                        [backup_pref_select, delete_backup_button_pref, restore_pref_button, backup_pref_button],
                        [backup_location_select],
                        [backup_location],
                        [warning_div],
                        [host_div],
                        [port_div],
                        [db_div]])

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Tabs and document
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
roi_tab = Panel(child=roi_layout, title='ROI Name Manager')
db_tab = Panel(child=db_editor_layout, title='Database Editor')
backup_tab = Panel(child=backup_layout, title='Backup & Restore')
baseline_tab = Panel(child=baseline_layout, title='Baseline Plans')

if options.DISABLE_BACKUP_TAB:
    tabs = Tabs(tabs=[db_tab, roi_tab, baseline_tab])
else:
    tabs = Tabs(tabs=[db_tab, roi_tab, baseline_tab, backup_tab])

# Create the document Bokeh server will use to generate the webpage
if ACCESS_GRANTED:
    curdoc().add_root(tabs)
else:
    curdoc().add_root(layout_login)

curdoc().title = "DVH Analytics: Admin"


if __name__ == '__main__':
    pass
