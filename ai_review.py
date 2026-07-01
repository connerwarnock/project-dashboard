import json
from datetime import datetime
from io import StringIO

import pandas as pd
import streamlit as st

from config import (
    AI_REVIEW_ACTIONS,
    AI_REVIEW_COLUMNS,
    AI_REVIEW_TARGETS,
    PROJECTS_WORKSHEET,
    PUBLISHING_QUEUE_WORKSHEET,
    SOURCE_RECORD_KEYS,
    TASKS_WORKSHEET,
)
from data_utils import (
    save_ai_review,
    save_projects,
    save_publishing_queue,
    save_tasks,
)
from sheets_utils import GoogleSheetsError


DATE_FIELDS = {
    PROJECTS_WORKSHEET: "Last Updated",
    TASKS_WORKSHEET: "Due Date",
    PUBLISHING_QUEUE_WORKSHEET: "Publish Date",
}


def current_timestamp():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def as_text(value):
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def as_boolean(value):
    if isinstance(value, bool):
        return value
    return as_text(value).lower() in {"true", "yes", "1", "checked"}


def normalize_review(review):
    normalized = review.copy()
    for column in AI_REVIEW_COLUMNS:
        if column not in normalized.columns:
            normalized[column] = False if column in {"Approved", "Applied"} else ""

    normalized = normalized[AI_REVIEW_COLUMNS].copy()
    for column in AI_REVIEW_COLUMNS:
        if column not in {"Approved", "Applied"}:
            normalized[column] = normalized[column].map(as_text)

    normalized["Approved"] = normalized["Approved"].map(as_boolean)
    normalized["Applied"] = normalized["Applied"].map(as_boolean)

    content_columns = [
        "Target Tab",
        "Action",
        "Record Key",
        "Field",
        "Current Value",
        "Suggested Value",
        "Reason",
    ]
    has_content = normalized[content_columns].apply(
        lambda row: any(as_text(value) for value in row),
        axis=1,
    )
    normalized = normalized[has_content].copy()

    missing_generated_at = normalized["Generated At"] == ""
    normalized.loc[missing_generated_at, "Generated At"] = current_timestamp()
    return normalized.reset_index(drop=True)


def parse_import_text(pasted_text):
    text = pasted_text.strip()
    if not text:
        raise ValueError("Paste JSON or CSV suggestions before importing.")

    if text.startswith("[") or text.startswith("{"):
        payload = json.loads(text)
        if isinstance(payload, dict) and "suggestions" in payload:
            payload = payload["suggestions"]
        elif isinstance(payload, dict):
            payload = [payload]
        if not isinstance(payload, list) or not all(
            isinstance(row, dict) for row in payload
        ):
            raise ValueError("JSON import must be an object or an array of objects.")
        imported = pd.DataFrame(payload)
    else:
        imported = pd.read_csv(StringIO(text), dtype=str, keep_default_na=False)

    unknown_columns = set(imported.columns) - set(AI_REVIEW_COLUMNS)
    if unknown_columns:
        names = ", ".join(sorted(unknown_columns))
        raise ValueError(f"Unknown AI Review columns: {names}.")

    if "Suggested Value" in imported.columns:
        imported["Suggested Value"] = imported["Suggested Value"].map(
            lambda value: json.dumps(value) if isinstance(value, dict) else value
        )

    imported = normalize_review(imported)
    if imported.empty:
        raise ValueError("No suggestion rows were found in the pasted content.")

    for index, row in imported.iterrows():
        if row["Target Tab"] not in AI_REVIEW_TARGETS:
            raise ValueError(
                f'Import row {index + 1} has an invalid Target Tab: "{row["Target Tab"]}".'
            )
        if row["Action"] not in AI_REVIEW_ACTIONS:
            raise ValueError(
                f'Import row {index + 1} has an invalid Action: "{row["Action"]}".'
            )

    imported["Approved"] = False
    imported["Applied"] = False
    imported["Applied At"] = ""
    return imported


def normalize_date(target, field, value):
    if field != DATE_FIELDS[target] or not value:
        return value
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        raise ValueError(f'"{value}" is not a valid date for {field}.')
    return parsed.strftime("%Y-%m-%d")


def apply_update(source, target, suggestion):
    key_column = SOURCE_RECORD_KEYS[target]
    record_key = as_text(suggestion["Record Key"])
    field = as_text(suggestion["Field"])

    if not record_key:
        raise ValueError("Record Key is required for updates.")
    if field not in source.columns:
        raise ValueError(f'Field "{field}" was not found in {target}.')

    matches = source[key_column].map(as_text) == record_key
    match_count = int(matches.sum())
    if match_count == 0:
        raise ValueError(f'{key_column} "{record_key}" was not found in {target}.')
    if match_count > 1:
        raise ValueError(f'{key_column} "{record_key}" is duplicated in {target}.')

    source_index = source.index[matches][0]
    actual_value = as_text(source.at[source_index, field])
    expected_value = as_text(suggestion["Current Value"])
    if actual_value != expected_value:
        raise ValueError(
            f'Current Value no longer matches for {record_key} / {field}. '
            f'Expected "{expected_value}" but found "{actual_value}".'
        )

    suggested_value = normalize_date(
        target,
        field,
        as_text(suggestion["Suggested Value"]),
    )
    if field == key_column:
        if not suggested_value:
            raise ValueError(f"{key_column} cannot be blank.")
        duplicate_key = source[key_column].map(as_text) == suggested_value
        duplicate_key.loc[source_index] = False
        if duplicate_key.any():
            raise ValueError(f'{key_column} "{suggested_value}" already exists in {target}.')

    source.at[source_index, field] = suggested_value


def apply_add(source, target, suggestion):
    try:
        row_data = json.loads(as_text(suggestion["Suggested Value"]))
    except json.JSONDecodeError as error:
        raise ValueError("Suggested Value for an add must be a valid JSON object.") from error

    if not isinstance(row_data, dict):
        raise ValueError("Suggested Value for an add must be a JSON object.")

    unknown_fields = set(row_data) - set(source.columns)
    if unknown_fields:
        names = ", ".join(sorted(unknown_fields))
        raise ValueError(f"Add contains fields not found in {target}: {names}.")

    new_row = {}
    for column in source.columns:
        value = row_data.get(column, "")
        if isinstance(value, (dict, list)):
            raise ValueError(f'Add field "{column}" must contain a simple value.')
        new_row[column] = as_text(value)

    date_field = DATE_FIELDS[target]
    new_row[date_field] = normalize_date(target, date_field, new_row[date_field])

    key_column = SOURCE_RECORD_KEYS[target]
    key_value = new_row[key_column]
    if not key_value:
        raise ValueError(f'Add JSON must include a nonblank "{key_column}" value.')

    review_key = as_text(suggestion["Record Key"])
    if review_key and review_key != key_value:
        raise ValueError(
            f'Record Key "{review_key}" does not match JSON {key_column} "{key_value}".'
        )
    if (source[key_column].map(as_text) == key_value).any():
        raise ValueError(f'{key_column} "{key_value}" already exists in {target}.')

    source.loc[len(source)] = [new_row[column] for column in source.columns]


def apply_approved_changes(review, projects, tasks, publishing_queue):
    normalized = normalize_review(review)
    sources = {
        PROJECTS_WORKSHEET: projects.copy(),
        TASKS_WORKSHEET: tasks.copy(),
        PUBLISHING_QUEUE_WORKSHEET: publishing_queue.copy(),
    }
    savers = {
        PROJECTS_WORKSHEET: save_projects,
        TASKS_WORKSHEET: save_tasks,
        PUBLISHING_QUEUE_WORKSHEET: save_publishing_queue,
    }
    valid_rows = {target: [] for target in AI_REVIEW_TARGETS}
    warnings = []

    pending = normalized[normalized["Approved"] & ~normalized["Applied"]]
    for index, suggestion in pending.iterrows():
        target = suggestion["Target Tab"]
        action = suggestion["Action"]
        row_label = f"Review row {index + 2}"

        if target not in sources:
            warnings.append(f'{row_label}: Target Tab "{target}" is not supported.')
            continue
        if action not in AI_REVIEW_ACTIONS:
            warnings.append(f'{row_label}: Action "{action}" is not supported.')
            continue

        try:
            if action == "Update existing record":
                apply_update(sources[target], target, suggestion)
            else:
                apply_add(sources[target], target, suggestion)
            valid_rows[target].append(index)
        except ValueError as error:
            warnings.append(f"{row_label}: {error}")

    applied_count = 0
    applied_at = current_timestamp()
    for target, row_indices in valid_rows.items():
        if not row_indices:
            continue
        try:
            savers[target](sources[target])
        except GoogleSheetsError as error:
            warnings.append(f"Could not save {target}: {error}")
            continue

        normalized.loc[row_indices, "Applied"] = True
        normalized.loc[row_indices, "Applied At"] = applied_at
        applied_count += len(row_indices)

    try:
        save_ai_review(normalized)
    except GoogleSheetsError as error:
        if applied_count:
            raise GoogleSheetsError(
                "Source changes were saved, but AI Review could not be marked as applied. "
                "Reload and verify the source sheets before trying again."
            ) from error
        raise
    return applied_count, warnings


def show_review_notice():
    notice = st.session_state.pop("ai_review_notice", None)
    if not notice:
        return
    if notice.get("message"):
        st.success(notice["message"])
    for warning in notice.get("warnings", []):
        st.warning(warning)


def render_ai_review(projects, tasks, publishing_queue, ai_review):
    st.subheader("🤖 AI Review")
    st.caption(
        "Human-approved staging for proposed project, task, and publishing changes."
    )
    st.info(
        "Imported suggestions never edit source sheets automatically. Approve the rows you "
        "want, then use Apply Approved Changes. Updates are skipped if Current Value no "
        "longer matches the source sheet."
    )
    show_review_notice()

    review = normalize_review(ai_review)
    pending_count = len(review[~review["Applied"]])
    approved_count = len(review[review["Approved"] & ~review["Applied"]])
    applied_count = len(review[review["Applied"]])

    col1, col2, col3 = st.columns(3)
    col1.metric("Pending Suggestions", pending_count)
    col2.metric("Approved, Not Applied", approved_count)
    col3.metric("Applied Suggestions", applied_count)

    with st.expander("Paste or import suggestions"):
        st.caption(
            "Paste a JSON object/array or CSV using AI Review column names. "
            "For Add new record, Suggested Value should be a JSON row object."
        )
        pasted_text = st.text_area(
            "Suggestion import",
            key="ai_review_import_text",
            height=180,
            placeholder='[{"Target Tab":"Projects","Action":"Update existing record",...}]',
            label_visibility="collapsed",
        )
        if st.button("Import suggestions", key="import_ai_review_button"):
            try:
                imported = parse_import_text(pasted_text)
                combined = pd.concat([review, imported], ignore_index=True)
                save_ai_review(normalize_review(combined))
                st.session_state["ai_review_notice"] = {
                    "message": f"Imported {len(imported)} suggestion(s) for review.",
                    "warnings": [],
                }
                st.rerun()
            except (ValueError, json.JSONDecodeError, pd.errors.ParserError) as error:
                st.error(f"Could not import suggestions: {error}")
            except GoogleSheetsError as error:
                st.error(str(error))

    edited_review = st.data_editor(
        review,
        key="ai_review_editor",
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        disabled=["Generated At", "Applied", "Applied At"],
        column_config={
            "Target Tab": st.column_config.SelectboxColumn(
                "Target Tab",
                options=AI_REVIEW_TARGETS,
            ),
            "Action": st.column_config.SelectboxColumn(
                "Action",
                options=AI_REVIEW_ACTIONS,
            ),
            "Approved": st.column_config.CheckboxColumn("Approved"),
            "Applied": st.column_config.CheckboxColumn("Applied"),
            "Suggested Value": st.column_config.TextColumn(
                "Suggested Value",
                width="large",
            ),
            "Reason": st.column_config.TextColumn("Reason", width="large"),
        },
    )

    save_col, apply_col = st.columns(2)
    with save_col:
        if st.button("Save review changes", key="save_ai_review_button"):
            try:
                save_ai_review(normalize_review(edited_review))
                st.session_state["ai_review_notice"] = {
                    "message": "AI Review changes saved. Source sheets were not changed.",
                    "warnings": [],
                }
                st.rerun()
            except GoogleSheetsError as error:
                st.error(str(error))

    with apply_col:
        if st.button(
            "Apply Approved Changes",
            key="apply_ai_review_button",
            type="primary",
        ):
            try:
                applied, warnings = apply_approved_changes(
                    edited_review,
                    projects,
                    tasks,
                    publishing_queue,
                )
                st.session_state["ai_review_notice"] = {
                    "message": f"Applied {applied} approved change(s).",
                    "warnings": warnings,
                }
                st.rerun()
            except GoogleSheetsError as error:
                st.error(str(error))
