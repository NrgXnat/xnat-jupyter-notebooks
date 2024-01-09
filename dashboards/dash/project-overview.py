# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import os
import xnat
import hvplot.pandas

port = 8050

jupyterhub_base_url = os.getenv('JUPYTERHUB_SERVICE_PREFIX') # /jupyterhub/user/{username}/

isJupyterLab = 'ServerApp' in os.environ.get('JUPYTERHUB_SINGLEUSER_APP','') # vs dashboard

# if running in JupyterLab, need to add proxy prefix to base URL
# e.g. /jupyterhub/user/{username}/proxy/{port}/ as expected by juptyer-server-proxy
# if running as a dashboard, jhsingle-native-proxy will use the base URL as is
if isJupyterLab:
    jupyterhub_base_url = f"{jupyterhub_base_url}proxy/{port}/"

app = Dash(
    __name__,
    requests_pathname_prefix=jupyterhub_base_url,
    external_stylesheets=[dbc.themes.CERULEAN]
)

xnat_host = os.getenv('XNAT_HOST')
xnat_user = os.getenv('XNAT_USER')
xnat_password = os.getenv('XNAT_PASS')

project_id = os.getenv('XNAT_ITEM_ID')

connection = xnat.connect(xnat_host, user=xnat_user, password=xnat_password)
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

subject_data = load_subject_data()
subject_data_df = pd.DataFrame(subject_data)

# Histogram of age distribution
fig_hist = px.histogram(subject_data_df, x='age', nbins=15, height=300, histfunc='count', title='Subject Age Distribution', labels={'age': 'Age (years)'})

# Create pie chart of gender distribution m vs f
genders = subject_data_df['gender'].value_counts()
fig_pie = px.pie(subject_data_df, values=genders.values, names=genders.index, title=f"Subject Genders")

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div(f"Project Overview for {project_id}", className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(data=subject_data_df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
        ], width=12),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_hist)
        ], width=6),
        dbc.Col([
            dcc.Graph(figure=fig_pie)
        ], width=6),
    ]),

], fluid=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
