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
            margin: 0.35rem 0 0.85rem;
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


def section_card(title):
    card = st.container(border=True)
    card.markdown(
        f'<div class="warm-future-section-header">{escape(title)}</div>',
        unsafe_allow_html=True,
    )
    return card


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
