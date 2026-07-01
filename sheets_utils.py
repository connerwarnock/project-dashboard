import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials


GOOGLE_SHEETS_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class GoogleSheetsError(RuntimeError):
    """A safe, user-facing Google Sheets error."""


@st.cache_resource
def get_spreadsheet():
    try:
        credentials = Credentials.from_service_account_info(
            dict(st.secrets["gcp_service_account"]),
            scopes=GOOGLE_SHEETS_SCOPES,
        )
        client = gspread.authorize(credentials)
        return client.open_by_key(st.secrets["spreadsheet_id"])
    except Exception as error:
        raise GoogleSheetsError(
            "Could not connect to Google Sheets. Check the Streamlit secrets "
            "and make sure the spreadsheet is shared with the service account."
        ) from error


def read_worksheet(worksheet_name):
    try:
        worksheet = get_spreadsheet().worksheet(worksheet_name)
        values = worksheet.get_all_values()
    except GoogleSheetsError:
        raise
    except Exception as error:
        raise GoogleSheetsError(
            f'Could not read the Google Sheets worksheet "{worksheet_name}".'
        ) from error

    if not values:
        return pd.DataFrame()

    return pd.DataFrame(values[1:], columns=values[0])


def fit_worksheet_row(row, width):
    fitted = list(row[:width])
    return fitted + [""] * (width - len(fitted))


def repair_worksheet_schema(worksheet, values, columns):
    width = len(columns)
    if not values:
        repaired_rows = []
    else:
        header = values[0]
        canonical_header = (
            header[:width] == columns and not any(header[width:])
        )
        if canonical_header:
            return [columns] + [fit_worksheet_row(row, width) for row in values[1:]]

        column_positions = {}
        for index, name in enumerate(header):
            if name in columns and name not in column_positions:
                column_positions[name] = index

        if column_positions:
            repaired_rows = []
            for row in values[1:]:
                repaired_rows.append(
                    [
                        row[column_positions[column]]
                        if column in column_positions
                        and column_positions[column] < len(row)
                        else ""
                        for column in columns
                    ]
                )
        else:
            repaired_rows = [fit_worksheet_row(row, width) for row in values]

    repaired_values = [columns] + repaired_rows
    required_rows = max(worksheet.row_count, len(repaired_values), 1)
    required_columns = max(worksheet.col_count, width)
    if required_rows != worksheet.row_count or required_columns != worksheet.col_count:
        worksheet.resize(rows=required_rows, cols=required_columns)

    worksheet.update(
        values=repaired_values,
        range_name="A1",
        value_input_option="RAW",
    )

    old_width = max((len(row) for row in values), default=0)
    if old_width > width:
        clear_start = gspread.utils.rowcol_to_a1(1, width + 1)
        clear_end = gspread.utils.rowcol_to_a1(len(repaired_values), old_width)
        worksheet.batch_clear([f"{clear_start}:{clear_end}"])

    return repaired_values


def read_or_create_worksheet(worksheet_name, columns):
    try:
        spreadsheet = get_spreadsheet()
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(
                title=worksheet_name,
                rows=100,
                cols=len(columns),
            )
        values = worksheet.get_all_values()
        values = repair_worksheet_schema(worksheet, values, columns)
    except GoogleSheetsError:
        raise
    except Exception as error:
        raise GoogleSheetsError(
            f'Could not prepare the Google Sheets worksheet "{worksheet_name}".'
        ) from error

    if len(values) == 1:
        return pd.DataFrame(columns=columns)

    return pd.DataFrame(values[1:], columns=values[0])


def write_worksheet(worksheet_name, dataframe):
    cleaned = dataframe.astype(object).where(pd.notna(dataframe), "")
    values = [cleaned.columns.tolist()] + cleaned.values.tolist()

    try:
        worksheet = get_spreadsheet().worksheet(worksheet_name)
        worksheet.clear()
        worksheet.update(
            values=values,
            range_name="A1",
            value_input_option="RAW",
        )
    except GoogleSheetsError:
        raise
    except Exception as error:
        raise GoogleSheetsError(
            f'Could not save the Google Sheets worksheet "{worksheet_name}".'
        ) from error
