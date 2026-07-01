import pandas as pd

from config import (
    AI_REVIEW_COLUMNS,
    AI_REVIEW_WORKSHEET,
    PROJECTS_WORKSHEET,
    PUBLISHING_QUEUE_WORKSHEET,
    TASKS_WORKSHEET,
)
from sheets_utils import read_or_create_worksheet, read_worksheet, write_worksheet


def load_projects():
    return read_worksheet(PROJECTS_WORKSHEET)


def load_tasks():
    return read_worksheet(TASKS_WORKSHEET)


def load_publishing_queue():
    return read_worksheet(PUBLISHING_QUEUE_WORKSHEET)


def load_ai_review():
    return read_or_create_worksheet(AI_REVIEW_WORKSHEET, AI_REVIEW_COLUMNS)


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


def save_ai_review(ai_review):
    review_to_save = ai_review.reindex(columns=AI_REVIEW_COLUMNS).copy()
    write_worksheet(AI_REVIEW_WORKSHEET, review_to_save)
