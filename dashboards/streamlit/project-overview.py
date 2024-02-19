import pandas as pd
import streamlit as st
import xnat
import os
import plotly.express as px
import matplotlib.pyplot as plt
import base64

# XNAT Setup
xnat_host = os.getenv('XNAT_HOST')
xnat_user = os.getenv('XNAT_USER')
xnat_password = os.getenv('XNAT_PASS')

if os.environ['XNAT_XSI_TYPE'] != 'xnat:projectData':
    raise Exception('Must be started from an XNAT project.')

project_id = os.getenv('XNAT_ITEM_ID')

connection = xnat.connect(xnat_host, user=xnat_user, password=xnat_password)
project = connection.projects[project_id]

@st.cache_data
def load_data(url):
    df = pd.read_csv(url, storage_options={"Authorization": b"Basic " + base64.b64encode(f"{xnat_user}:{xnat_password}".encode())})
    return df

@st.cache_data
def get_subject_data():
    url = f"{xnat_host}/data/projects/{project_id}/subjects?format=csv&columns=age,gender"
    df = load_data(url)
    df = df.drop(columns=['URI'])
    return df

# Start Streamlit
st.title(f"Subject demographics for project {project_id}")

st.write("This is a demo of a Streamlit app that shows subject demographics for a project in XNAT.")

st.markdown("### Subject data")

# Show a table of subject data
df = get_subject_data()
st.dataframe(df, width=700, height=300)

# Histogram of ages
st.markdown("## Histogram of ages")
st.markdown("### Using Plotly")
fig1 = px.histogram(df, x="age")
fig1.update_layout(bargap=0.2)
st.plotly_chart(fig1)

# Pie chart of genders
st.markdown("## Pie chart of genders")
st.markdown("### Using Matplotlib")
fig2, ax = plt.subplots()
df['gender'].value_counts().plot.pie(ax=ax, autopct='%1.1f%%')
st.pyplot(fig2)
