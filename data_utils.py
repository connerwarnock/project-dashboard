import pandas as pd

from config import (
    PROJECTS_WORKSHEET,
    PUBLISHING_QUEUE_WORKSHEET,
    TASKS_WORKSHEET,
)
from sheets_utils import read_worksheet, write_worksheet


def load_projects():
    return read_worksheet(PROJECTS_WORKSHEET)


def load_tasks():
    return read_worksheet(TASKS_WORKSHEET)


def load_publishing_queue():
    return read_worksheet(PUBLISHING_QUEUE_WORKSHEET)


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
    write_worksheet(PROJECTS_WORKSHEET, projects_to_save)


def save_tasks(tasks):
    tasks_to_save = format_date_column(tasks, "Due Date")
    write_worksheet(TASKS_WORKSHEET, tasks_to_save)


def save_publishing_queue(publishing_queue):
    queue_to_save = format_date_column(publishing_queue, "Publish Date")
    write_worksheet(PUBLISHING_QUEUE_WORKSHEET, queue_to_save)
