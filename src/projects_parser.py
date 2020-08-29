#!/usr/bin/env python3

import json
import re

from utils import pick_keys

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
            if len(match) == 0:
                # assign None as "not found" value
                match = None
        else:
            match = match[0]
        project[detail] = match
    return project

def split_supervisor_and_description(project, supervisor_descr_separator='\n'):
    """
    Split the combined supervisor and description field into separate fields.
    Use the separator to differentiate supervisor from description.
    """
    if 'supervisor_and_description' not in project:
        anomaly_warning('SUPERVISOR AND DESCRIPTION SPLIT', '"supervisor_and_description" key is missing', project)
        return project
    supervisor_and_description = project['supervisor_and_description']
    idx = supervisor_and_description.find(supervisor_descr_separator)
    if idx == -1:
        anomaly_warning('SUPERVISOR AND DESCRIPTION SPLIT', supervisor_and_description, idx)
        # leave project unmodified
        return project
    else:
        split = idx+len(supervisor_descr_separator)
        supervisor = supervisor_and_description[:split]
        description = supervisor_and_description[split:]
        # delete old key and add two new keys
        del project['supervisor_and_description']
        return {**project, 'supervisor': supervisor, 'description': description}

def parse_student_details(project, name_sep='Name', email_sep='Email'):
    """
    Parse unstructured student data into a structured data.
    """
    if 'students' not in project:
        anomaly_warning('STUDENT PARSING', '"students" key is missing', project)
        return project
    students = project['students']
    parsed_students = []
    if not isinstance(students, str):
        anomaly_warning('STUDENT PARSING', 'students is not a string field', project, students)
        return project

    for stud in students.split(name_sep):
        s = stud.split(email_sep)
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

def canonicalize_projects(projects, **kwargs):
    """Transform projects to a standard (canonical) form.
       kwargs are passed to functions with extra arguments.
    """
    canonical_projects = []
    for project in projects:
        canon = split_supervisor_and_description(project, **pick_keys(kwargs, ['supervisor_descr_separator']))
        canon = parse_student_details(canon, **pick_keys(kwargs, ['name_sep', 'email_sep']))
        canon = remove_newlines(canon)
        canonical_projects.append(canon)
    return canonical_projects

def apply_transformation(projects, fn, *args, **kwargs):
    """
    Utility function to apply the function fn to every project in projects.
    Additional arguments are passed to fn.
    fn must return a complete project object.
    """
    return [fn(project, *args, **kwargs) for project in projects]

def write_json(booklet_year, projects_obj):
    """Write projects_obj as a JSON file for a given year"""
    with open('../booklets_data/{}.json'.format(booklet_year), 'w', encoding='utf-8') as f:
        json.dump(projects_obj, f, ensure_ascii=False, indent=4, sort_keys=True)
