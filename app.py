import streamlit as st

from dashboard_views import (
    render_dashboard,
    render_edit_projects,
    render_edit_tasks,
    render_publishing_queue,
)
from data_utils import load_projects, load_publishing_queue, load_tasks
from sheets_utils import GoogleSheetsError


st.set_page_config(page_title="Project Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("Project Dashboard")
st.caption("A simple command center for tracking projects, tasks, and publishing ideas.")

try:
    projects = load_projects()
    tasks = load_tasks()
    publishing_queue = load_publishing_queue()
except GoogleSheetsError as error:
    st.error(str(error))
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Edit Projects", "Edit Tasks", "Publishing Queue", "View Dashboard"]
)

with tab1:
    render_edit_projects(projects)

with tab2:
    render_edit_tasks(projects, tasks)

with tab3:
    render_publishing_queue(projects, publishing_queue)

with tab4:
    render_dashboard(projects, tasks, publishing_queue)
