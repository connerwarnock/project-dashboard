import pandas as pd

from config import PROJECTS_CSV, TASKS_CSV


def load_projects():
    return pd.read_csv(PROJECTS_CSV)


def load_tasks():
    return pd.read_csv(TASKS_CSV)


def parse_date_column(dataframe, column_name):
    cleaned = dataframe.copy()
    cleaned[column_name] = pd.to_datetime(cleaned[column_name], errors="coerce")
    return cleaned


def format_date_column(dataframe, column_name):
    cleaned = dataframe.copy()
    cleaned[column_name] = (
        pd.to_datetime(cleaned[column_name], errors="coerce")
        .dt.strftime("%Y-%m-%d")
        .fillna("")
    )
    return cleaned


def save_projects(projects):
    projects_to_save = format_date_column(projects, "Last Updated")
    projects_to_save.to_csv(PROJECTS_CSV, index=False)


def save_tasks(tasks):
    tasks_to_save = format_date_column(tasks, "Due Date")
    tasks_to_save.to_csv(TASKS_CSV, index=False)
