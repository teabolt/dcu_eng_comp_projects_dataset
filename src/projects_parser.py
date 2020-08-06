#!/usr/bin/env python3

import json
import re

def anomaly_warning(anomaly, *args):
    print('{} ANOMALY: {}'.format(anomaly, ' '.join(map(str, args))))

def parse_projects(project_list):
    projects = []
    for idx, project_string in enumerate(project_list):
        title = re.findall(r'(?s)Project Title(.*?)Name', project_string)
        if len(title) != 1:
            anomaly_warning('PROJECT TITLE', idx, project_string, title)
        else:
            title = title[0]

        students = re.findall(r'Name(.*?)Programme', project_string, flags=re.S)
        if len(students) != 1:
            anomaly_warning('STUDENTS', idx, project_string, students)
        else:
            students = students[0]

        programme = re.findall(r'Programme(.*)Supervisor', project_string, flags=re.S)
        if len(programme) != 1:
            anomaly_warning('PROGRAMME', idx, project_string, programme)
        else:
            programme = programme[0]
            
        supervisor_and_description = re.findall(r'Supervisor(.*)Project Video', project_string, flags=re.S)
        if len(supervisor_and_description) != 1:
            anomaly_warning('SUPERVISOR AND DESCRIPTION', idx, project_string, supervisor_and_description)
        else:
            supervisor_and_description = supervisor_and_description[0]

        video = re.findall(r'Project Video(.*?)Project Area', project_string, flags=re.S)
        if len(video) != 1:
            anomaly_warning('VIDEO', idx, project_string, video)
        else:
            video = video[0]

        area = re.findall(r'Project Area(.*?)Project Technology', project_string, flags=re.S)
        if len(area) != 1:
            anomaly_warning('AREA', idx, project_string, area)
        else:
            area = area[0]

        technology = re.findall(r'Project Technology(.*?)$', project_string, flags=re.S)
        if len(technology) != 1:
            anomaly_warning('TECHNOLOGY', idx, project_string, technology)
        else:
            technology = technology[0]

        projects.append({
            'title': title,
            'students': students,
            'programme': programme,
            'supervisor_and_description': supervisor_and_description,
            'video': video,
            'area': area,
            'technology': technology,
        })
    return projects
    
def split_supervisor_and_description(supervisor_and_description):
    res = supervisor_and_description.split('@dcu.ie')
    if len(res) != 2:
        anomaly_warning('SUPERVISOR AND DESCRIPTION', supervisor_and_description, res)
        return None, None
    else:
        supervisor, description = res
        supervisor = supervisor + '@dcu.ie'
        return supervisor.strip(), description.strip()

def normalize_students(students):
    normalized = []
    for stud in students.split('Name'):
        s = stud.split('Email')
        if len(s) != 2:
            print('STUDENT NORMALIZATION ANOMALY: {}, {}, {}'.format(students, stud, s))
            continue
        name, email = s
        normalized.append({
            'name': name.strip(),
            'email': email.strip(),
        })
    return normalized

def normalize_projects(projects):
    normalized_projects = []
    for project in projects:
        supervisor, description = split_supervisor_and_description(project['supervisor_and_description'])
        normalized_projects.append({
            'title': project['title'].strip(),
            'students': normalize_students(project['students']),
            'programme': project['programme'].strip(),
            'supervisor': supervisor,
            'description': description,
            'video': project['video'].strip(),
            'area': project['area'].strip(),
            'technology': project['technology'].strip(),
        })
    return normalized_projects

def write_json(booklet_year, projects_obj):
    with open('../booklets_data/{}.json'.format(booklet_year), 'w') as f:
        json.dump(projects_obj, f, indent=4)
