import panel as pn
import os 
import pandas as pd
import xnat

import plotly.express as px
import hvplot.pandas

pn.extension('plotly')

# XNAT setup
xnat_host = os.getenv('XNAT_HOST')
xnat_user = os.getenv('XNAT_USER')
xnat_password = os.getenv('XNAT_PASS')

project_id = os.environ['XNAT_ITEM_ID']

connection = xnat.connect(xnat_host, user=xnat_user, password=xnat_password, loglevel='INFO')
project = connection.projects[project_id]

def load_subject_data():

    subject_data = {
        'id': [],
        'gender': [],
        'age': []
    }

    for subject in project.subjects.values():
        subject_data['id'].append(subject.label)
        subject_data['gender'].append(subject.demographics.gender)
        subject_data['age'].append(subject.demographics.age)

    return subject_data


# Panel setup
template = pn.template.BootstrapTemplate(
    title=f'Project Overview for {project_id}',
    busy_indicator=pn.indicators.BooleanStatus(value=False)
)

loading = pn.indicators.LoadingSpinner(value=False, width=100, height=100,visible=False)
main_column = pn.Column(loading)

template.main.append(
    pn.Row(
        main_column,
        sizing_mode="stretch_both",
    )
)

#function to activate / deactivate loading widget      
def load_display(x):
    if(x=='on'):
        loading.value=True
        loading.visible=True
    if(x=='off'):
        loading.value=False
        loading.visible=False

def display_subject_data():
    load_display('on')

    subject_data = load_subject_data()
    df = pd.DataFrame(subject_data)
    df_pane = pn.pane.DataFrame(df, sizing_mode="stretch_both", max_height=250)

    title = pn.pane.Markdown("### Subjects")
    main_column.append(title)
    main_column.append(df_pane)

    # Histogram of age distribution
    histogram_age = df.hvplot.hist('age', bins=15, height=300)
    histogram_age.opts(xlabel='Age', ylabel='Count')
    histogram_age.opts(width=500, height=300)

    # Create pie chart of gender distribution m vs f
    genders = df['gender'].value_counts()
    fig = px.pie(df, values=genders.values, names=genders.index)

    main_column.append(
        pn.Row(
            pn.Column(
                pn.pane.Markdown(f"### Subject Age Distribution"),
                histogram_age
            ),
            pn.Column(
                pn.pane.Markdown(f"### Gender Distribution"),
                fig
            )
        )
    )

    load_display('off')

pn.state.onload(display_subject_data)

template.servable()
