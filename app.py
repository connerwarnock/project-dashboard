from datetime import datetime

import streamlit as st

from dashboard_views import (
    render_dashboard,
    render_edit_projects,
    render_edit_tasks,
    render_publishing_queue,
)
from data_utils import load_projects, load_publishing_queue, load_tasks
from sheets_utils import GoogleSheetsError
from ui_styles import (
    apply_warm_future_theme,
    render_app_header,
    render_footer,
    render_sidebar,
)


st.set_page_config(
    page_title="Project Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_warm_future_theme()

render_app_header(
    "Lost Nomad Dashboard",
    "A Warm Future workspace for research, charts, and public writing.",
)

try:
    projects = load_projects()
    tasks = load_tasks()
    publishing_queue = load_publishing_queue()
except GoogleSheetsError as error:
    st.error(str(error))
    st.stop()

refreshed_at = datetime.now().astimezone()
last_refreshed = (
    f"{refreshed_at:%Y-%m-%d} "
    f"{refreshed_at.strftime('%I:%M %p').lstrip('0')}"
)
render_sidebar(last_refreshed)

overview_tab, projects_tab, tasks_tab, publish_tab = st.tabs(
    ["📊 Overview", "📁 Projects", "✅ Tasks", "📝 Publish"]
)

with overview_tab:
    render_dashboard(projects, tasks, publishing_queue)

with projects_tab:
    render_edit_projects(projects)

with tasks_tab:
    render_edit_tasks(projects, tasks)

with publish_tab:
    render_publishing_queue(projects, publishing_queue)

render_footer()
