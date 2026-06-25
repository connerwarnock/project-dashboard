import streamlit as st
import pandas as pd
from datetime import datetime

PROJECTS_CSV = "projects.csv"
TASKS_CSV = "tasks.csv"

PROJECT_STATUSES = ["Backlog", "Active", "Paused", "Needs Review", "Ready to Publish", "Shipped", "Archived", "Reference"]
TASK_STATUSES = ["Not Started", "Doing", "Blocked", "Paused", "Done"]
PRIORITIES = ["High", "Medium", "Low"]

st.set_page_config(page_title="Project Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("Project Dashboard")
st.caption("A simple command center for tracking projects, tasks, and publishing ideas.")

projects = pd.read_csv(PROJECTS_CSV)
tasks = pd.read_csv(TASKS_CSV)

tab1, tab2, tab3 = st.tabs(["Edit Projects", "Edit Tasks", "View Dashboard"])

with tab1:
    st.subheader("Edit Projects")

    projects_for_edit = projects.copy()
    projects_for_edit["Last Updated"] = pd.to_datetime(
        projects_for_edit["Last Updated"],
        errors="coerce"
    )

    edited_projects = st.data_editor(
        projects_for_edit,
        key="projects_editor",
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "Status": st.column_config.SelectboxColumn("Status", options=PROJECT_STATUSES),
            "Priority": st.column_config.SelectboxColumn("Priority", options=PRIORITIES),
            "Last Updated": st.column_config.DateColumn("Last Updated", format="YYYY-MM-DD"),
        }
    )

    if st.button("Save project changes", key="save_projects_button"):
        edited_projects["Last Updated"] = (
            pd.to_datetime(edited_projects["Last Updated"], errors="coerce")
            .dt.strftime("%Y-%m-%d")
            .fillna("")
        )

        edited_projects.to_csv(PROJECTS_CSV, index=False)
        st.success("Project changes saved.")

with tab2:
    st.subheader("Edit Tasks")

    project_options = projects["Project"].dropna().unique().tolist()
    tasks_for_edit = tasks.copy()
    tasks_for_edit["Due Date"] = pd.to_datetime(tasks_for_edit["Due Date"], errors="coerce")

    edited_tasks = st.data_editor(
        tasks_for_edit,
        key="tasks_editor",
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "Project": st.column_config.SelectboxColumn("Project", options=project_options),
            "Status": st.column_config.SelectboxColumn("Status", options=TASK_STATUSES),
            "Priority": st.column_config.SelectboxColumn("Priority", options=PRIORITIES),
            "Due Date": st.column_config.DateColumn("Due Date", format="YYYY-MM-DD"),
        }
    )    

    if st.button("Save task changes", key="save_tasks_button"):
        edited_tasks["Due Date"] = (
            pd.to_datetime(edited_tasks["Due Date"], errors="coerce")
            .dt.strftime("%Y-%m-%d")
            .fillna("")
        )

        edited_tasks.to_csv(TASKS_CSV, index=False)
        st.success("Task changes saved.")

with tab3:
    tasks["Due Date Parsed"] = pd.to_datetime(tasks["Due Date"], errors="coerce")
    today = pd.Timestamp.today().normalize()

    active_count = len(projects[projects["Status"] == "Active"])
    open_tasks = tasks[tasks["Status"] != "Done"].copy()
    overdue_tasks = open_tasks[
        open_tasks["Due Date Parsed"].notna() &
        (open_tasks["Due Date Parsed"] < today)
    ]
    upcoming_tasks = open_tasks[
        open_tasks["Due Date Parsed"].notna() &
        (open_tasks["Due Date Parsed"] >= today)
    ].sort_values("Due Date Parsed")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Projects", active_count)
    col2.metric("Open Tasks", len(open_tasks))
    col3.metric("High-Priority Open Tasks", len(open_tasks[open_tasks["Priority"] == "High"]))
    col4.metric("Overdue Tasks", len(overdue_tasks))

    st.subheader("Projects Overview")

    projects_overview = projects[projects["Status"] != "Archived"].copy()
    projects_overview["Last Updated"] = (
        pd.to_datetime(projects_overview["Last Updated"], errors="coerce")
        .dt.strftime("%Y-%m-%d")
        .fillna("")
    )

    st.dataframe(
        projects_overview[
            ["Project", "Category", "Status", "Priority", "Stage", "Next Action", "Last Updated"]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Stale Projects")

    projects_with_dates = projects.copy()
    projects_with_dates["Last Updated Parsed"] = pd.to_datetime(
        projects_with_dates["Last Updated"],
        errors="coerce"
    )

    stale_cutoff = today - pd.Timedelta(days=14)

    stale_projects = projects_with_dates[
        projects_with_dates["Status"].isin(["Active", "Paused", "Needs Review"]) &
        projects_with_dates["Last Updated Parsed"].notna() &
        (projects_with_dates["Last Updated Parsed"] < stale_cutoff)
    ]

    st.dataframe(
        stale_projects.drop(columns=["Last Updated Parsed"], errors="ignore"),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Next Actions")

    next_actions = open_tasks[
        open_tasks["Status"].isin(["Not Started", "Doing", "Blocked"]) &
        open_tasks["Priority"].isin(["High", "Medium"])
    ].copy()

    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    status_order = {"Doing": 1, "Blocked": 2, "Not Started": 3, "Paused": 4, "Done": 5}

    next_actions["Priority Rank"] = next_actions["Priority"].map(priority_order)
    next_actions["Status Rank"] = next_actions["Status"].map(status_order)

    next_actions = next_actions.sort_values(
        by=["Priority Rank", "Status Rank", "Due Date Parsed"],
        na_position="last"
    ).drop(columns=["Priority Rank", "Status Rank", "Due Date Parsed"])

    st.dataframe(next_actions, use_container_width=True, hide_index=True)

    st.subheader("Overdue Tasks")
    st.dataframe(overdue_tasks.drop(columns=["Due Date Parsed"]), use_container_width=True, hide_index=True)

    st.subheader("Upcoming Deadlines")
    st.dataframe(upcoming_tasks.drop(columns=["Due Date Parsed"]), use_container_width=True, hide_index=True)

    st.subheader("Project Detail")

    selected_project_detail = st.selectbox(
        "Choose a project to inspect",
        project_options,
        key="project_detail_select"
    )

    project_row = projects[projects["Project"] == selected_project_detail]
    project_tasks = tasks[tasks["Project"] == selected_project_detail]

    if not project_row.empty:
        project_info = project_row.iloc[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Status", project_info["Status"])
        col2.metric("Priority", project_info["Priority"])
        col3.metric("Stage", project_info["Stage"])

        st.write("**Next Action:**", project_info["Next Action"])
        st.write("**Last Updated:**", project_info.get("Last Updated", ""))

        st.write("**Project Tasks**")
        st.dataframe(
            project_tasks.drop(columns=["Due Date Parsed"], errors="ignore"),
            use_container_width=True,
            hide_index=True
        )
