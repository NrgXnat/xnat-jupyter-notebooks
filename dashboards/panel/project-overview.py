import os

import numpy as np
import pandas as pd
import xnat

import hvplot.pandas
import panel as pn
import plotly.express as px

pn.extension('plotly')

# XNAT setup
xnat_host = os.getenv('XNAT_HOST')
xnat_user = os.getenv('XNAT_USER')
xnat_password = os.getenv('XNAT_PASS')

if os.environ['XNAT_XSI_TYPE'] != 'xnat:projectData':
    raise Exception('Must be started from an XNAT project.')

project_id = os.getenv('XNAT_ITEM_ID')

connection = xnat.connect(xnat_host, user=xnat_user, password=xnat_password)
project = connection.projects[project_id]

# Cache for subject data
subject_data_cache = None

# Compile subject data or return cached data
def get_subject_data():
    global subject_data_cache
    
    if subject_data_cache is not None:
        return subject_data_cache
    
    subject_data = {
        'id': [],
        'gender': [],
        'age': []
    }

    for subject in project.subjects.values():
        subject_data['id'].append(subject.label)
        subject_data['gender'].append(subject.demographics.gender)
        subject_data['age'].append(subject.demographics.age)
        
    df = pd.DataFrame(subject_data)
    
    subject_data_cache = df

    return df


# Panel setup
pn.extension(design='material')

# Subject data table
df = get_subject_data()
df_pane = pn.pane.DataFrame(df, sizing_mode="stretch_both", max_height=500)

# Histogram of age distribution
histogram_age = df.hvplot.hist('age', bins=15, height=300)
histogram_age.opts(xlabel='Age', ylabel='Count')
histogram_age.opts(width=500, height=300)

# Create pie chart of gender distribution m vs f
genders = get_subject_data()['gender'].value_counts()
fig = px.pie(df, values=genders.values, names=genders.index)

app = pn.Column(
    pn.pane.Markdown(f"# Subject demographics for project {project_id}"),
    df_pane,
    histogram_age,
    fig,
    sizing_mode="stretch_both",
    max_height=500
)

app.servable()
