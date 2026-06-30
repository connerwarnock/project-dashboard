from html import escape

import streamlit as st


STATUS_BADGE_STYLES = {
    "Active": ("#E6F8F6", "#63D5D0"),
    "Doing": ("#FBE8ED", "#E56B8A"),
    "In Progress": ("#FBE8ED", "#E56B8A"),
    "Ready": ("#E5F7EE", "#8ADDBA"),
    "Ready to Publish": ("#E5F7EE", "#8ADDBA"),
    "Done": ("#E5F7EE", "#8ADDBA"),
    "Published": ("#E5F7EE", "#8ADDBA"),
    "Shipped": ("#E5F7EE", "#8ADDBA"),
    "Drafting": ("#EEEAFB", "#B8A7E8"),
    "Needs Review": ("#EEEAFB", "#B8A7E8"),
    "Needs Visual": ("#EEEAFB", "#B8A7E8"),
    "Paused": ("#F3EFEC", "#D8CCC3"),
    "Backlog": ("#F3EFEC", "#D8CCC3"),
    "Archived": ("#F3EFEC", "#D8CCC3"),
    "Blocked": ("#FCEAE8", "#F2A6A0"),
    "Overdue": ("#FCEAE8", "#F2A6A0"),
    "Reference": ("#FFF6D8", "#F7D97A"),
}
DEFAULT_STATUS_BADGE_STYLE = ("#F3EFEC", "#D8CCC3")


def apply_warm_future_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --warm-background: #FFF9F4;
            --warm-surface: #FFFCF9;
            --warm-text: #2F2A28;
            --warm-muted: #6F6865;
            --warm-border: #EADBD4;
            --warm-pink: #E56B8A;
            --warm-turquoise: #63D5D0;
            --warm-yellow: #F7D97A;
            --warm-mint: #8ADDBA;
            --warm-lavender: #B8A7E8;
            --warm-gray: #D8CCC3;
            --warm-coral: #F2A6A0;
        }

        .stApp {
            background-color: var(--warm-background);
            color: var(--warm-text);
            font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI",
                sans-serif;
        }

        .stApp button,
        .stApp input,
        .stApp textarea,
        .stApp select {
            font-family: inherit;
        }

        [data-testid="stHeader"] {
            background-color: rgba(255, 249, 244, 0.94);
        }

        h1, h2, h3 {
            color: var(--warm-text);
            letter-spacing: 0;
        }

        [data-testid="stMetricLabel"] {
            color: var(--warm-muted);
        }

        .warm-future-header {
            margin-bottom: 0.4rem;
            padding: 0.35rem 0 1rem;
            border-bottom: 1px solid var(--warm-border);
        }

        .warm-future-title {
            margin: 0;
            color: var(--warm-text);
            font-size: 2.15rem;
            font-weight: 700;
            line-height: 1.2;
        }

        .warm-future-title-rule {
            width: 52px;
            height: 4px;
            margin: 0.65rem 0 0.7rem;
            border-radius: 2px;
            background-color: var(--warm-turquoise);
        }

        .warm-future-subtitle {
            margin: 0;
            color: var(--warm-muted);
            font-size: 0.98rem;
            line-height: 1.5;
        }

        .warm-command-center {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin: 0.3rem 0 1.1rem;
            padding: 1rem 1.1rem;
            background-color: var(--warm-surface);
            border: 1px solid var(--warm-border);
            border-left: 4px solid var(--warm-turquoise);
            border-radius: 8px;
            box-shadow: 0 4px 14px rgba(71, 56, 50, 0.045);
        }

        .warm-command-center h2 {
            margin: 0 0 0.3rem;
            font-size: 1.35rem;
            font-weight: 650;
            line-height: 1.3;
        }

        .warm-command-center p {
            margin: 0;
            color: var(--warm-muted);
            font-size: 0.92rem;
            line-height: 1.45;
        }

        .warm-state-list {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-end;
            gap: 0.4rem;
            max-width: 360px;
        }

        .warm-state-badge {
            padding: 0.24rem 0.55rem;
            color: var(--warm-text);
            background-color: #F3EFEC;
            border: 1px solid var(--warm-gray);
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            line-height: 1.25;
            white-space: nowrap;
        }

        .warm-state-badge.is-active {
            background-color: #E6F8F6;
            border-color: var(--warm-turquoise);
        }

        .warm-state-badge.is-ready,
        .warm-state-badge.is-published {
            background-color: #E5F7EE;
            border-color: var(--warm-mint);
        }

        .warm-state-badge.is-paused {
            background-color: #F3EFEC;
            border-color: var(--warm-gray);
        }

        .warm-state-badge.is-blocked,
        .warm-state-badge.is-overdue {
            background-color: #FCEAE8;
            border-color: var(--warm-coral);
        }

        [data-testid="stMetric"] {
            position: relative;
            min-height: 116px;
            padding: 1rem 1.1rem 1rem 1.25rem;
            overflow: hidden;
            background-color: var(--warm-surface);
            border: 1px solid var(--warm-border);
            border-radius: 8px;
            box-shadow: 0 4px 14px rgba(71, 56, 50, 0.055);
        }

        [data-testid="stMetric"]::before {
            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            width: 4px;
            background-color: var(--warm-pink);
            content: "";
        }

        [data-testid="stMetricValue"] {
            color: var(--warm-text);
            font-weight: 700;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.25rem;
            border-bottom: 1px solid var(--warm-border);
        }

        .stTabs button[data-baseweb="tab"] {
            padding: 0.7rem 1rem;
            color: var(--warm-muted);
            border-radius: 8px 8px 0 0;
        }

        .stTabs button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--warm-text);
            background-color: rgba(229, 107, 138, 0.09);
        }

        .stTabs [data-baseweb="tab-highlight"] {
            background-color: var(--warm-pink);
        }

        [data-testid="stDataFrame"],
        [data-testid="stDataEditor"] {
            border: 1px solid var(--warm-border);
            border-radius: 8px;
            box-shadow: 0 3px 12px rgba(71, 56, 50, 0.04);
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            padding: 1rem;
            margin: 0.45rem 0 1.05rem;
            background-color: var(--warm-surface);
            border-color: var(--warm-border) !important;
            border-radius: 8px;
            box-shadow: 0 3px 14px rgba(71, 56, 50, 0.045);
        }

        .warm-future-section-header {
            margin: 0.1rem 0 0.9rem;
            padding-left: 0.65rem;
            color: var(--warm-text);
            border-left: 4px solid var(--warm-turquoise);
            font-size: 1.2rem;
            font-weight: 600;
            line-height: 1.35;
        }

        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] {
            margin: -0.35rem 0 0.55rem;
            color: var(--warm-muted);
        }

        .warm-empty-state {
            padding: 0.9rem 1rem;
            color: var(--warm-muted);
            background-color: rgba(99, 213, 208, 0.07);
            border: 1px dashed #B7E9E5;
            border-radius: 8px;
            font-size: 0.9rem;
            line-height: 1.45;
        }

        @media (max-width: 700px) {
            .warm-command-center {
                align-items: flex-start;
                flex-direction: column;
            }

            .warm-state-list {
                justify-content: flex-start;
                max-width: none;
            }
        }

        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMetric"] {
            min-height: 96px;
            padding: 0.65rem 0.8rem;
            background-color: transparent;
            border: 0;
            border-left: 3px solid var(--warm-pink);
            border-radius: 0;
            box-shadow: none;
        }

        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMetric"]::before {
            display: none;
        }

        [data-testid="stSidebar"] {
            background-color: var(--warm-surface);
            border-right: 1px solid var(--warm-border);
        }

        [data-testid="stSidebarContent"] {
            padding-top: 1.4rem;
        }

        .warm-sidebar-brand {
            margin-bottom: 1rem;
            padding: 0.2rem 0.15rem 1rem;
            border-bottom: 1px solid var(--warm-border);
        }

        .warm-sidebar-brand h2 {
            margin: 0;
            color: var(--warm-text);
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1.3;
        }

        .warm-sidebar-brand-rule {
            width: 36px;
            height: 3px;
            margin: 0.55rem 0 0.6rem;
            background-color: var(--warm-turquoise);
            border-radius: 2px;
        }

        .warm-sidebar-brand p {
            margin: 0;
            color: var(--warm-muted);
            font-size: 0.84rem;
        }

        .warm-sidebar-label {
            margin: 0 0 0.55rem;
            color: var(--warm-muted);
            font-size: 0.73rem;
            font-weight: 700;
        }

        .warm-sidebar-nav {
            display: grid;
            gap: 0.3rem;
            margin-bottom: 1rem;
        }

        .warm-sidebar-nav-item {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            padding: 0.4rem 0.45rem;
            color: var(--warm-text);
            border-radius: 6px;
            font-size: 0.86rem;
            font-weight: 500;
        }

        .warm-sidebar-dot {
            width: 8px;
            height: 8px;
            flex: 0 0 8px;
            background-color: var(--warm-gray);
            border-radius: 50%;
        }

        .warm-sidebar-dot.is-projects {
            background-color: var(--warm-pink);
        }

        .warm-sidebar-dot.is-tasks {
            background-color: var(--warm-turquoise);
        }

        .warm-sidebar-dot.is-publishing {
            background-color: var(--warm-lavender);
        }

        .warm-sidebar-dot.is-dashboard {
            background-color: var(--warm-yellow);
        }

        .warm-sidebar-meta,
        .warm-sidebar-workflow {
            margin-bottom: 0.8rem;
            padding: 0.8rem;
            background-color: var(--warm-background);
            border: 1px solid var(--warm-border);
            border-radius: 8px;
        }

        .warm-sidebar-meta-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            color: var(--warm-muted);
            font-size: 0.78rem;
        }

        .warm-sidebar-meta-row + .warm-sidebar-meta-row {
            margin-top: 0.55rem;
            padding-top: 0.55rem;
            border-top: 1px solid var(--warm-border);
        }

        .warm-sidebar-meta-row strong {
            color: var(--warm-text);
            font-weight: 600;
            text-align: right;
        }

        .warm-sidebar-connected {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.18rem 0.42rem;
            color: var(--warm-text);
            background-color: #E5F7EE;
            border: 1px solid var(--warm-mint);
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 600;
        }

        .warm-sidebar-connected::before {
            width: 6px;
            height: 6px;
            background-color: var(--warm-mint);
            border-radius: 50%;
            content: "";
        }

        .warm-sidebar-workflow p {
            margin: 0;
            color: var(--warm-text);
            font-size: 0.82rem;
            font-weight: 600;
            line-height: 1.55;
        }

        .warm-sidebar-workflow span {
            color: var(--warm-pink);
        }

        .stButton > button {
            color: var(--warm-text);
            background-color: var(--warm-surface);
            border-color: var(--warm-pink);
            border-radius: 8px;
        }

        .stButton > button:hover {
            color: var(--warm-text);
            background-color: rgba(229, 107, 138, 0.08);
            border-color: var(--warm-pink);
        }

        hr {
            border-color: var(--warm-border);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_app_header(title, subtitle):
    safe_title = escape(title)
    safe_subtitle = escape(subtitle)

    st.markdown(
        f"""
        <div class="warm-future-header">
            <h1 class="warm-future-title">{safe_title}</h1>
            <div class="warm-future-title-rule"></div>
            <p class="warm-future-subtitle">{safe_subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    st.sidebar.markdown(
        """
        <div class="warm-sidebar-brand">
            <h2>Project Dashboard</h2>
            <div class="warm-sidebar-brand-rule"></div>
            <p>Personal command center</p>
        </div>

        <p class="warm-sidebar-label">MAIN SECTIONS</p>
        <div class="warm-sidebar-nav" aria-label="Main sections">
            <div class="warm-sidebar-nav-item">
                <span class="warm-sidebar-dot is-projects"></span>Projects
            </div>
            <div class="warm-sidebar-nav-item">
                <span class="warm-sidebar-dot is-tasks"></span>Tasks
            </div>
            <div class="warm-sidebar-nav-item">
                <span class="warm-sidebar-dot is-publishing"></span>Publishing Queue
            </div>
            <div class="warm-sidebar-nav-item">
                <span class="warm-sidebar-dot is-dashboard"></span>Dashboard
            </div>
        </div>

        <p class="warm-sidebar-label">APP STATUS</p>
        <div class="warm-sidebar-meta">
            <div class="warm-sidebar-meta-row">
                <span>Data source</span><strong>Google Sheets</strong>
            </div>
            <div class="warm-sidebar-meta-row">
                <span>Storage</span><span class="warm-sidebar-connected">Connected</span>
            </div>
        </div>

        <p class="warm-sidebar-label">WORKFLOW</p>
        <div class="warm-sidebar-workflow">
            <p>Plan <span>&rarr;</span> Build <span>&rarr;</span> Publish <span>&rarr;</span> Review</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard_hero():
    st.markdown(
        """
        <div class="warm-command-center">
            <div>
                <h2>Project Command Center</h2>
                <p>Track active work, deadlines, publishing, and next actions.</p>
            </div>
            <div class="warm-state-list" aria-label="Key workflow states">
                <span class="warm-state-badge is-active">Active</span>
                <span class="warm-state-badge is-paused">Paused</span>
                <span class="warm-state-badge is-blocked">Blocked</span>
                <span class="warm-state-badge is-ready">Ready</span>
                <span class="warm-state-badge is-published">Published</span>
                <span class="warm-state-badge is-overdue">Overdue</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_card(title):
    card = st.container(border=True)
    card.markdown(
        f'<div class="warm-future-section-header">{escape(title)}</div>',
        unsafe_allow_html=True,
    )
    return card


def render_empty_state(container, message):
    container.markdown(
        f'<div class="warm-empty-state">{escape(message)}</div>',
        unsafe_allow_html=True,
    )


def style_status_badges(dataframe):
    if "Status" not in dataframe.columns:
        return dataframe

    def status_style(value):
        background, border = STATUS_BADGE_STYLES.get(
            value,
            DEFAULT_STATUS_BADGE_STYLE,
        )

        return (
            f"background-color: {background}; "
            f"border: 1px solid {border}; "
            "color: #2F2A28; "
            "font-weight: 600; "
            "text-align: center; "
            "border-radius: 6px;"
        )

    return dataframe.style.apply(
        lambda statuses: [status_style(status) for status in statuses],
        subset=["Status"],
    )
