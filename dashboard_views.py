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
    render_active_project_cards,
    render_about_dashboard,
    render_dashboard_hero,
    render_empty_state,
    render_mini_stats,
    render_project_progress,
    render_publishing_pipeline,
    render_weekly_pulse,
    section_card,
    style_table_indicators,
)


def render_edit_projects(projects):
    st.subheader("✏️ Edit Projects")
    st.caption("Update project status, stage, priority, and next actions.")

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
    st.subheader("✅ Edit Tasks")
    st.caption("Manage task status, priority, and deadlines.")

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
    st.subheader("📝 Publishing Queue")
    st.caption("Plan and track outputs from idea through publication.")

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
    paused_count = len(projects[projects["Status"] == "Paused"])
    shipped_count = len(projects[projects["Status"] == "Shipped"])
    open_tasks = tasks[tasks["Status"] != "Done"].copy()
    overdue_tasks = open_tasks[
        open_tasks["Due Date Parsed"].notna()
        & (open_tasks["Due Date Parsed"] < today)
    ]
    upcoming_tasks = open_tasks[
        open_tasks["Due Date Parsed"].notna()
        & (open_tasks["Due Date Parsed"] >= today)
    ].sort_values("Due Date Parsed")
    stale_projects = get_stale_projects(projects, today)
    ready_output_count = len(publishing_queue[publishing_queue["Status"] == "Ready"])
    high_priority_count = len(open_tasks[open_tasks["Priority"] == "High"])

    render_dashboard_hero()
    render_weekly_pulse(
        active_projects=active_count,
        open_tasks=len(open_tasks),
        high_priority_tasks=high_priority_count,
        overdue_tasks=len(overdue_tasks),
        upcoming_deadlines=len(upcoming_tasks),
        ready_outputs=ready_output_count,
        stale_projects=len(stale_projects),
    )
    render_active_projects(projects)
    render_recently_updated(projects)
    render_publishing_summary(publishing_queue, ready_output_count)
    render_projects_overview(projects, active_count, paused_count, shipped_count)
    render_stale_projects(stale_projects)
    render_next_actions(open_tasks, high_priority_count, len(overdue_tasks))
    render_deadlines(overdue_tasks, upcoming_tasks)
    render_project_detail(projects, tasks, project_options)
    render_about_dashboard()


def get_project_options(projects):
    return projects["Project"].dropna().unique().tolist()


def count_label(count, singular, plural=None):
    if count == 1:
        return singular
    return plural or f"{singular}s"


def get_stale_projects(projects, today):
    projects_with_dates = projects.copy()
    projects_with_dates["Last Updated Parsed"] = pd.to_datetime(
        projects_with_dates["Last Updated"],
        errors="coerce",
    )
    stale_cutoff = today - pd.Timedelta(days=14)

    return projects_with_dates[
        projects_with_dates["Status"].isin(["Active", "Paused", "Needs Review"])
        & projects_with_dates["Last Updated Parsed"].notna()
        & (projects_with_dates["Last Updated Parsed"] < stale_cutoff)
    ]


def render_dashboard_table(card, dataframe, empty_message):
    if dataframe.empty:
        render_empty_state(card, empty_message)
        return

    card.dataframe(
        style_table_indicators(dataframe),
        use_container_width=True,
        hide_index=True,
    )


def render_active_projects(projects):
    active_projects = projects[projects["Status"] == "Active"].copy()
    active_projects = format_date_column(active_projects, "Last Updated")
    active_records = active_projects.fillna("").to_dict("records")
    render_active_project_cards(active_records)


def render_recently_updated(projects):
    card = section_card("Recently Updated", "🕘", "lavender")
    card.caption("The five projects with the most recent recorded updates.")

    recent_projects = projects.copy()
    recent_projects["Last Updated Parsed"] = pd.to_datetime(
        recent_projects["Last Updated"],
        errors="coerce",
    )
    recent_projects = recent_projects[
        recent_projects["Last Updated Parsed"].notna()
    ].sort_values("Last Updated Parsed", ascending=False).head(5)
    recent_projects = recent_projects.drop(columns=["Last Updated Parsed"])
    recent_projects = format_date_column(recent_projects, "Last Updated")

    render_dashboard_table(
        card,
        recent_projects[["Project", "Category", "Status", "Stage", "Last Updated"]],
        "No project updates have been dated yet.",
    )


def render_publishing_summary(publishing_queue, ready_output_count):
    card = section_card("Publishing Queue Summary", "📝", "lavender")
    card.caption("A quick pulse on what is moving toward publication.")

    unpublished = publishing_queue[
        ~publishing_queue["Status"].isin(["Published", "Archived"])
    ]
    drafting_count = len(publishing_queue[publishing_queue["Status"] == "Drafting"])
    published = publishing_queue[publishing_queue["Status"] == "Published"]

    render_mini_stats(
        card,
        [
            (drafting_count, count_label(drafting_count, "draft")),
            (ready_output_count, count_label(ready_output_count, "ready", "ready")),
            (len(published), count_label(len(published), "published", "published")),
        ],
    )
    render_publishing_pipeline(
        card,
        publishing_queue["Status"].value_counts().to_dict(),
    )

    col1, col2, col3 = card.columns(3)
    col1.metric("Unpublished Outputs", len(unpublished))
    col2.metric("Ready to Publish", ready_output_count)
    col3.metric("Published Outputs", len(published))


def render_projects_overview(projects, active_count, paused_count, shipped_count):
    card = section_card("Projects Overview", "📁", "turquoise")
    card.caption("All current projects at a glance.")

    projects_overview = projects[projects["Status"] != "Archived"].copy()
    projects_overview = format_date_column(projects_overview, "Last Updated")

    render_mini_stats(
        card,
        [
            (active_count, count_label(active_count, "active", "active")),
            (paused_count, count_label(paused_count, "paused", "paused")),
            (shipped_count, count_label(shipped_count, "shipped", "shipped")),
        ],
    )

    render_dashboard_table(
        card,
        projects_overview[PROJECT_OVERVIEW_COLUMNS],
        "No current projects to show yet.",
    )


def render_stale_projects(stale_projects):
    card = section_card("Stale Projects", "🕒", "gray")
    card.caption("Active work not updated in the last 14 days.")

    render_dashboard_table(
        card,
        stale_projects.drop(columns=["Last Updated Parsed"], errors="ignore"),
        "No stale projects. Everything is moving.",
    )


def render_next_actions(open_tasks, high_priority_count, overdue_count):
    card = section_card("Next Actions", "📌", "pink")
    card.caption("High- and medium-priority work that needs attention.")
    render_mini_stats(
        card,
        [
            (len(open_tasks), count_label(len(open_tasks), "open", "open")),
            (
                high_priority_count,
                count_label(high_priority_count, "high priority", "high priority"),
            ),
            (overdue_count, count_label(overdue_count, "overdue", "overdue")),
        ],
    )

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
    overdue_card = section_card("Overdue Tasks", "🚨", "coral")
    overdue_card.caption("Open tasks that have passed their due date.")
    render_dashboard_table(
        overdue_card,
        overdue_tasks.drop(columns=["Due Date Parsed"]),
        "No overdue tasks. Nice.",
    )

    upcoming_card = section_card("Upcoming Deadlines", "⏰", "yellow")
    upcoming_card.caption("Open tasks with due dates ahead.")
    render_dashboard_table(
        upcoming_card,
        upcoming_tasks.drop(columns=["Due Date Parsed"]),
        "No upcoming deadlines on the calendar.",
    )


def render_project_detail(projects, tasks, project_options):
    card = section_card("Project Detail", "🧭", "mint")
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

        render_project_progress(
            card,
            project_info["Status"],
            project_info["Stage"],
        )

        card.write(f"**Next Action:** {project_info['Next Action']}")
        card.write(f"**Last Updated:** {project_info.get('Last Updated', '')}")

        card.write("**Project Tasks**")
        render_dashboard_table(
            card,
            project_tasks.drop(columns=["Due Date Parsed"], errors="ignore"),
            "No tasks for this project yet.",
        )
