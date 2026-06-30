# Project Dashboard

A personal Streamlit dashboard for tracking projects, tasks, publishing outputs, next actions, deadlines, and stale projects.

Live data is stored in these Google Sheets worksheets:

- `Projects`
- `Tasks`
- `Publishing Queue`

The local CSV files remain in the repository as backups:

- `projects.csv`
- `tasks.csv`
- `publishing_queue.csv`

Google Sheets access is configured with the `spreadsheet_id` and
`gcp_service_account` entries in Streamlit secrets. Keep the secrets file local
and do not commit it to version control.

## Run locally

```bash
streamlit run app.py
```
