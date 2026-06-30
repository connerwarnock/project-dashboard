import pandas as pd
import streamlit as st

from config import (
    PRIORITIES,
    PROJECT_OVERVIEW_COLUMNS,
    PROJECT_STATUSES,
    PUBLISHING_FORMATS,
    PUBLISHING_STATUSES,
    TARGET_PLATFORMS,
    TASK_STATUSES,
    VISUAL_READY_OPTIONS,
)
from data_utils import (
    format_date_column,
    parse_date_column,
    save_projects,
    save_publishing_queue,
    save_tasks,
)
from sheets_utils import GoogleSheetsError
from ui_styles import (
    render_dashboard_hero,
    render_empty_state,
    section_card,
    style_status_badges,
)


def render_edit_projects(projects):
    st.subheader("Edit Projects")

    projects_for_edit = parse_date_column(projects, "Last Updated")

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
        },
    )

    if st.button("Save project changes", key="save_projects_button"):
        try:
            save_projects(edited_projects)
            st.success("Project changes saved.")
        except GoogleSheetsError as error:
            st.error(str(error))


def render_edit_tasks(projects, tasks):
    st.subheader("Edit Tasks")

    project_options = get_project_options(projects)
    tasks_for_edit = parse_date_column(tasks, "Due Date")

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
        },
    )

    if st.button("Save task changes", key="save_tasks_button"):
        try:
            save_tasks(edited_tasks)
            st.success("Task changes saved.")
        except GoogleSheetsError as error:
            st.error(str(error))


def render_publishing_queue(projects, publishing_queue):
    st.subheader("Publishing Queue")

    project_options = get_project_options(projects)
    queue_for_edit = parse_date_column(publishing_queue, "Publish Date")

    edited_queue = st.data_editor(
        queue_for_edit,
        key="publishing_queue_editor",
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "Project": st.column_config.SelectboxColumn("Project", options=project_options),
            "Format": st.column_config.SelectboxColumn("Format", options=PUBLISHING_FORMATS),
            "Status": st.column_config.SelectboxColumn("Status", options=PUBLISHING_STATUSES),
            "Visual Ready": st.column_config.SelectboxColumn(
                "Visual Ready",
                options=VISUAL_READY_OPTIONS,
            ),
            "Target Platform": st.column_config.SelectboxColumn(
                "Target Platform",
                options=TARGET_PLATFORMS,
            ),
            "Publish Date": st.column_config.DateColumn(
                "Publish Date",
                format="YYYY-MM-DD",
            ),
        },
    )

    if st.button("Save publishing queue", key="save_publishing_queue_button"):
        try:
            save_publishing_queue(edited_queue)
            st.success("Publishing queue saved.")
        except GoogleSheetsError as error:
            st.error(str(error))


def render_dashboard(projects, tasks, publishing_queue):
    project_options = get_project_options(projects)
    tasks = tasks.copy()
    tasks["Due Date Parsed"] = pd.to_datetime(tasks["Due Date"], errors="coerce")
    today = pd.Timestamp.today().normalize()

    active_count = len(projects[projects["Status"] == "Active"])
    open_tasks = tasks[tasks["Status"] != "Done"].copy()
    overdue_tasks = open_tasks[
        open_tasks["Due Date Parsed"].notna()
        & (open_tasks["Due Date Parsed"] < today)
    ]
    upcoming_tasks = open_tasks[
        open_tasks["Due Date Parsed"].notna()
        & (open_tasks["Due Date Parsed"] >= today)
    ].sort_values("Due Date Parsed")

    render_dashboard_hero()
    render_metrics(active_count, open_tasks, overdue_tasks)
    render_publishing_summary(publishing_queue)
    render_projects_overview(projects)
    render_stale_projects(projects, today)
    render_next_actions(open_tasks)
    render_deadlines(overdue_tasks, upcoming_tasks)
    render_project_detail(projects, tasks, project_options)


def get_project_options(projects):
    return projects["Project"].dropna().unique().tolist()


def render_dashboard_table(card, dataframe, empty_message):
    if dataframe.empty:
        render_empty_state(card, empty_message)
        return

    card.dataframe(
        style_status_badges(dataframe),
        use_container_width=True,
        hide_index=True,
    )


def render_metrics(active_count, open_tasks, overdue_tasks):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Projects", active_count)
    col2.metric("Open Tasks", len(open_tasks))
    col3.metric("High-Priority Open Tasks", len(open_tasks[open_tasks["Priority"] == "High"]))
    col4.metric("Overdue Tasks", len(overdue_tasks))


def render_publishing_summary(publishing_queue):
    card = section_card("Publishing Queue Summary")
    card.caption("A quick pulse on what is moving toward publication.")

    unpublished = publishing_queue[
        ~publishing_queue["Status"].isin(["Published", "Archived"])
    ]
    ready = publishing_queue[publishing_queue["Status"] == "Ready"]
    published = publishing_queue[publishing_queue["Status"] == "Published"]

    col1, col2, col3 = card.columns(3)
    col1.metric("Unpublished Outputs", len(unpublished))
    col2.metric("Ready to Publish", len(ready))
    col3.metric("Published Outputs", len(published))


def render_projects_overview(projects):
    card = section_card("Projects Overview")
    card.caption("All current projects at a glance.")

    projects_overview = projects[projects["Status"] != "Archived"].copy()
    projects_overview = format_date_column(projects_overview, "Last Updated")

    render_dashboard_table(
        card,
        projects_overview[PROJECT_OVERVIEW_COLUMNS],
        "No current projects to show yet.",
    )


def render_stale_projects(projects, today):
    card = section_card("Stale Projects")
    card.caption("Active work not updated in the last 14 days.")

    projects_with_dates = projects.copy()
    projects_with_dates["Last Updated Parsed"] = pd.to_datetime(
        projects_with_dates["Last Updated"],
        errors="coerce",
    )

    stale_cutoff = today - pd.Timedelta(days=14)

    stale_projects = projects_with_dates[
        projects_with_dates["Status"].isin(["Active", "Paused", "Needs Review"])
        & projects_with_dates["Last Updated Parsed"].notna()
        & (projects_with_dates["Last Updated Parsed"] < stale_cutoff)
    ]

    render_dashboard_table(
        card,
        stale_projects.drop(columns=["Last Updated Parsed"], errors="ignore"),
        "No stale projects. Everything is moving.",
    )


def render_next_actions(open_tasks):
    card = section_card("Next Actions")
    card.caption("High- and medium-priority work that needs attention.")

    next_actions = open_tasks[
        open_tasks["Status"].isin(["Not Started", "Doing", "Blocked"])
        & open_tasks["Priority"].isin(["High", "Medium"])
    ].copy()

    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    status_order = {"Doing": 1, "Blocked": 2, "Not Started": 3, "Paused": 4, "Done": 5}

    next_actions["Priority Rank"] = next_actions["Priority"].map(priority_order)
    next_actions["Status Rank"] = next_actions["Status"].map(status_order)

    next_actions = next_actions.sort_values(
        by=["Priority Rank", "Status Rank", "Due Date Parsed"],
        na_position="last",
    ).drop(columns=["Priority Rank", "Status Rank", "Due Date Parsed"])

    render_dashboard_table(
        card,
        next_actions,
        "No priority next actions right now.",
    )


def render_deadlines(overdue_tasks, upcoming_tasks):
    overdue_card = section_card("Overdue Tasks")
    overdue_card.caption("Open tasks that have passed their due date.")
    render_dashboard_table(
        overdue_card,
        overdue_tasks.drop(columns=["Due Date Parsed"]),
        "No overdue tasks. Nice.",
    )

    upcoming_card = section_card("Upcoming Deadlines")
    upcoming_card.caption("Open tasks with due dates ahead.")
    render_dashboard_table(
        upcoming_card,
        upcoming_tasks.drop(columns=["Due Date Parsed"]),
        "No upcoming deadlines on the calendar.",
    )


def render_project_detail(projects, tasks, project_options):
    card = section_card("Project Detail")
    card.caption("Inspect the current focus and task list for one project.")

    selected_project_detail = card.selectbox(
        "Choose a project to inspect",
        project_options,
        key="project_detail_select",
    )

    project_row = projects[projects["Project"] == selected_project_detail]
    project_tasks = tasks[tasks["Project"] == selected_project_detail]

    if not project_row.empty:
        project_info = project_row.iloc[0]

        col1, col2, col3 = card.columns(3)
        col1.metric("Status", project_info["Status"])
        col2.metric("Priority", project_info["Priority"])
        col3.metric("Stage", project_info["Stage"])

        card.write(f"**Next Action:** {project_info['Next Action']}")
        card.write(f"**Last Updated:** {project_info.get('Last Updated', '')}")

        card.write("**Project Tasks**")
        render_dashboard_table(
            card,
            project_tasks.drop(columns=["Due Date Parsed"], errors="ignore"),
            "No tasks for this project yet.",
        )
