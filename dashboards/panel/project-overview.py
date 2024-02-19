import panel as pn
import os 
import pandas as pd
import xnat
import base64

import plotly.express as px
import hvplot.pandas

pn.extension('plotly', defer_load=True, loading_indicator=True)

# XNAT setup
xnat_host = os.getenv('XNAT_HOST')
xnat_user = os.getenv('XNAT_USER')
xnat_password = os.getenv('XNAT_PASS')

project_id = os.environ['XNAT_ITEM_ID']

connection = xnat.connect(xnat_host, user=xnat_user, password=xnat_password, loglevel='INFO')
project = connection.projects[project_id]

def load_data(url):
    df = pd.read_csv(url, storage_options={"Authorization": b"Basic " + base64.b64encode(f"{xnat_user}:{xnat_password}".encode())})
    return df

def load_subject_data():
    url = f"{xnat_host}/data/projects/{project_id}/subjects?format=csv&columns=age,gender"
    df = load_data(url)
    df = df.drop(columns=['URI'])
    return df

container = pn.Column()

title = pn.pane.Markdown(
    f"# Project Overview for {project_id}",
)

title_row = pn.Row(
    title,
)

container.append(title_row)

inner = pn.Column()

loading = pn.pane.Markdown("Loading...")
inner.append(loading)

container.append(inner)

def display_subject_data():

    loading.object = "Loading subject data..."

    subject_data = load_subject_data()

    loading.object = "### Subjects"

    df = pd.DataFrame(subject_data)
    df_pane = pn.pane.DataFrame(df, max_rows=15)

    inner.append(df_pane)

    # Histogram of age distribution
    inner.append(pn.pane.Markdown(f"### Subject Age Distribution"))
    
    histogram_age = df.hvplot.hist('age', bins=15, height=300)
    histogram_age.opts(xlabel='Age', ylabel='Count')
    histogram_age.opts(width=500, height=300)
    
    inner.append(histogram_age)
    
    # Create pie chart of gender distribution m vs f
    inner.append(pn.pane.Markdown(f"### Gender Distribution"))
    
    genders = df['gender'].value_counts()
    genders_fig = px.pie(df, values=genders.values, names=genders.index)
    
    inner.append(genders_fig)
    
pn.state.onload(display_subject_data)

container.servable()
