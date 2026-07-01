# Project Dashboard Handoff

## 1. Project Summary

- Personal Streamlit project dashboard.
- Deployed on Streamlit Cloud.
- Code lives on GitHub.
- Persistent data lives in Google Sheets.
- Codex is used to edit and implement the app.
- ChatGPT is used for planning, explanations, QA, and prompt-writing.

## 2. Key Links and Paths

- GitHub repository: [connerwarnock/project-dashboard](https://github.com/connerwarnock/project-dashboard)
- Streamlit app: [project-dashboard-6cnynplmjpjnwwbssmermg.streamlit.app](https://project-dashboard-6cnynplmjpjnwwbssmermg.streamlit.app)
- Google Sheet: [Project Dashboard data](https://docs.google.com/spreadsheets/d/1V6SUafWU7u6wHR34PV1TkhKSz-SV1FniaBDnbudsB7A/edit)
- Local project path: `C:\Users\torto\Desktop\project-dashboard`

The Google Sheet should remain private. Only the user and the app's service
account should have access.

## 3. Current Workflow

1. Plan changes in ChatGPT.
2. Generate a precise implementation prompt in ChatGPT.
3. Implement code changes in Codex.
4. Test locally before committing.
5. Commit and push the changes to GitHub.
6. Streamlit Cloud redeploys from GitHub.
7. Google Sheets stores persistent app data.

## 4. Local Setup Commands

Run these commands from a terminal:

```powershell
cd Desktop\project-dashboard
conda activate project-dashboard
streamlit run app.py
```

## 5. Git Workflow

Always check `git status` before every commit. A normal workflow is:

```powershell
git status
git add .
git commit -m "Describe change"
git push
```

Review the files listed by `git status` before staging so secrets, local files,
or unrelated changes are not committed accidentally.

## 6. Data and Storage

Google Sheets contains these worksheet tabs:

- `Projects`
- `Tasks`
- `Publishing Queue`

The app also creates and uses an `AI Review` worksheet as a staging area. The
three worksheets above remain the source of truth.

The local CSV files remain as backups only. The app reads and writes Google
Sheets through service account credentials.

- Local secrets live in `.streamlit/secrets.toml`.
- Deployed secrets live in Streamlit Cloud secrets.
- Never commit secrets, credential JSON files, or private keys.

## 7. Security Notes

- `.streamlit/secrets.toml` is ignored by Git.
- The service account should have access only to the shared dashboard Google
  Sheet.
- Never paste or print secrets in logs, documentation, Codex output, or
  ChatGPT.
- The public Streamlit app should not contain sensitive or private information
  unless access controls are added later.

## 8. Design Style

The app uses the Warm Future house style. See [`DESIGN.md`](DESIGN.md) for the
full design notes.

- Official font: Inter, with system sans-serif fallbacks.
- Background: `#FFF9F4`
- Text: `#2F2A28`
- Primary pink: `#E56B8A`
- Accent turquoise: `#63D5D0`
- Soft yellow: `#F7D97A`
- Mint green: `#8ADDBA`
- Lavender: `#B8A7E8`
- Warm gray: `#D8CCC3`
- Soft coral: `#F2A6A0`
- Feel: clean, warm, modern, lightweight, and lightly optimistic.
- Use a short turquoise accent rule near major titles where appropriate.
- Lost Nomad branding uses a turquoise horizon, pink sun, and subtle route-line
  motif to connect public writing, optimistic futures, navigation, and data.

## 9. User Preferences

- Assume beginner-level coding and Git knowledge.
- Give clear, step-by-step instructions.
- Prefer small, safe changes.
- Avoid large architectural rewrites unless explicitly requested.
- Keep the app lightweight and easy to use.
- Visual polish matters because a pleasant, low-friction dashboard is more
  likely to be used consistently.
- Use Codex mainly for code implementation.
- Use ChatGPT for planning, explanations, QA, and prompt production.

## 10. Current App Features

- Editable Projects table.
- Editable Tasks table.
- Editable Publishing Queue.
- Overview is the first and default landing tab, followed by Projects, Tasks,
  Publish, and AI Review.
- Projects Overview.
- Active Project cards and Recently Updated appear near the top of Overview.
- Stale Projects.
- Next Actions.
- Overdue Tasks.
- Upcoming Deadlines.
- Publishing summary.
- Publishing pipeline for Idea, Drafting, Needs Visual, Ready, and Published.
- Weekly Pulse overview strip.
- Project Detail.
- Lost Nomad branding in the main header, dashboard hero, and sidebar.
- Warm Future styling.
- Lightweight icons in tabs, section headers, and the sidebar.
- Sidebar with app metadata and workflow.
- Sidebar status legend, section mini stats, and About dashboard card.
- Sidebar North Star tagline: "Build the future, track the work."
- Google Sheets persistence.
- Human-approved AI Review staging and apply workflow.

## 11. Good Future Improvements

- Add an Ideas Backlog.
- Add an Assets tracker.
- Add access control or a private deployment.
- Improve charts and dashboard summaries.
- Add tests or lightweight validation.

## 12. AI Review Workflow

AI Review stages proposed changes before they reach source worksheets. It is not
an autonomous editor, and importing or approving a row does not apply it.

The `AI Review` worksheet uses these columns:

- `Generated At`
- `Target Tab`
- `Action`
- `Record Key`
- `Field`
- `Current Value`
- `Suggested Value`
- `Reason`
- `Approved`
- `Applied`
- `Applied At`

Supported actions are `Update existing record` and `Add new record`. Updates
identify a source row by its key (`Project`, `Task`, or `Output`) and apply only
when `Current Value` still exactly matches the source. Adds use a JSON object in
`Suggested Value`, with keys matching the target worksheet's existing columns.

Suggestions can be pasted into the app as a JSON object, JSON array, or CSV
using the AI Review column names. Imported rows are always reset to unapproved
and unapplied. The user must check `Approved` and click `Apply Approved Changes`.
Successful rows are marked `Applied` with an `Applied At` timestamp; invalid or
stale rows remain unapplied and produce warnings.
