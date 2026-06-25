import streamlit as st

from dashboard_views import render_dashboard, render_edit_projects, render_edit_tasks
from data_utils import load_projects, load_tasks


st.set_page_config(page_title="Project Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("Project Dashboard")
st.caption("A simple command center for tracking projects, tasks, and publishing ideas.")

projects = load_projects()
tasks = load_tasks()

tab1, tab2, tab3 = st.tabs(["Edit Projects", "Edit Tasks", "View Dashboard"])

with tab1:
    render_edit_projects(projects)

with tab2:
    render_edit_tasks(projects, tasks)

with tab3:
    render_dashboard(projects, tasks)
