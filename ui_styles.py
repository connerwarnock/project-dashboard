from html import escape

import streamlit as st


def apply_warm_future_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --warm-background: #FFF9F4;
            --warm-surface: #FFFCF9;
            --warm-text: #343130;
            --warm-muted: #6F6865;
            --warm-border: #EADBD4;
            --warm-pink: #E56B8A;
            --warm-turquoise: #63D5D0;
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
            background-color: #F5ECE7;
            border: 1px solid var(--warm-border);
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            line-height: 1.25;
            white-space: nowrap;
        }

        .warm-state-badge.is-active,
        .warm-state-badge.is-ready,
        .warm-state-badge.is-published {
            background-color: #DDF7F5;
            border-color: #B7E9E5;
        }

        .warm-state-badge.is-paused {
            background-color: #F5ECE7;
        }

        .warm-state-badge.is-blocked,
        .warm-state-badge.is-overdue {
            background-color: #FBE6EC;
            border-color: #F3C4D1;
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

    positive_statuses = {
        "Active",
        "Doing",
        "Done",
        "Published",
        "Ready",
        "Ready to Publish",
        "Shipped",
    }
    attention_statuses = {"Blocked", "Needs Review", "Needs Visual", "Paused"}

    def status_style(value):
        if value in positive_statuses:
            background = "#DDF7F5"
        elif value in attention_statuses:
            background = "#FBE6EC"
        else:
            background = "#F5ECE7"

        return (
            f"background-color: {background}; "
            "color: #343130; "
            "font-weight: 600; "
            "text-align: center; "
            "border-radius: 6px;"
        )

    return dataframe.style.apply(
        lambda statuses: [status_style(status) for status in statuses],
        subset=["Status"],
    )
