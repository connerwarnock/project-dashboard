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
