#!/usr/bin/env python3

import json
import re


def anomaly_warning(anomaly, *args):
    """Print a warning for anomaly, with optional strings to print"""
    print('{} ANOMALY: {}'.format(anomaly, ' '.join(map(str, args))))

def parse_projects(project_list, regex_schema):
    """
    project_list is a list of strings, where each string is a single project's details (unstructured).
    regex_schema is a dictionary from project details to regular expressions that should match that detail.
    
    returns a list of structured objects with each project's parsed (matched) details.
    """
    # compile all regexes
    compiled = {k: re.compile(regex, flags=re.S)
                              for k, regex in regex_schema.items()}
    # extract details of all projects into a list
    return [parse_project(project_string, compiled, idx) for idx, project_string in enumerate(project_list)]


def parse_project(project_string, compiled, idx=''):
    """
    extract details of a single project
    project_string - string containing all project information
    compiled - dictionary of detail names to compiled regular expressions that provide those details
    idx - project number as a string for debugging purposes, optional

    returns a dictionary from detail keys to the matched detail values.
    """
    project = {}
    for detail, pattern in compiled.items():
        match = pattern.findall(project_string)
        if len(match) != 1:
            anomaly_warning(detail, idx, project_string)
        else:
            match = match[0]
        project[detail] = match
    return project

def apply_transformation(projects, fn, *args, **kwargs):
    """
    Apply the function fn to every project in projects. Additional arguments are passed to fn.
    fn must return a complete project object.
    """
    return [fn(project, *args, **kwargs) for project in projects]

def split_supervisor_and_description(project, separator='@dcu.ie'):
    """
    Split the combined supervisor and description field into separate fields.
    Use the separator to differentiate supervisor from description.
    """
    supervisor_and_description = project['supervisor_and_description']
    idx = supervisor_and_description.find(separator)
    if idx == -1:
        anomaly_warning('SUPERVISOR AND DESCRIPTION SPLIT', supervisor_and_description, res)
        # leave project unmodified
        return project
    else:
        split = idx+len(separator)
        supervisor = supervisor_and_description[:split]
        description = supervisor_and_description[split:]
        # delete old key and add two new keys
        del project['supervisor_and_description']
        return {**project, 'supervisor': supervisor, 'description': description}

def parse_student_details(project):
    """
    Parse unstructured student data into a structured data.
    """
    students = project['students']
    parsed_students = []
    for stud in students.split('Name'):
        s = stud.split('Email')
        if len(s) != 2:
            anomaly_warning('STUDENT PARSING', students, stud, s)
            continue
        name, email = s
        parsed_students.append({
            'name': name.strip(),
            'email': email.strip(),
        })
    return {**project, 'students': parsed_students}

def remove_newlines(project):
    """
    Strip and replace newlines in project details.
    """
    return { k: v.strip().replace('\n', ' ') if type(v) == str else v for k, v in project.items()}

def write_json(booklet_year, projects_obj):
    """Write projects_obj as a JSON file for a given year"""
    with open('../booklets_data/{}.json'.format(booklet_year), 'w') as f:
        json.dump(projects_obj, f, indent=4, sort_keys=True)
