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

STAGE_BADGE_STYLES = {
    "Planning": ("#FFF6D8", "#F7D97A"),
    "Research": ("#EEEAFB", "#B8A7E8"),
    "Dataset": ("#E6F8F6", "#63D5D0"),
    "Charting": ("#FBE8ED", "#E56B8A"),
    "Editing": ("#EEEAFB", "#B8A7E8"),
    "Review": ("#EEEAFB", "#B8A7E8"),
    "Ready": ("#E5F7EE", "#8ADDBA"),
    "Publishing": ("#E5F7EE", "#8ADDBA"),
    "Reference": ("#FFF6D8", "#F7D97A"),
}
DEFAULT_STAGE_BADGE_STYLE = ("#F3EFEC", "#D8CCC3")

PROJECT_STATUS_PROGRESS = {
    "Backlog": 1,
    "Active": 2,
    "Paused": 2,
    "Needs Review": 3,
    "Ready to Publish": 4,
    "Shipped": 4,
    "Archived": 4,
    "Reference": 1,
}

PROJECT_STAGE_PROGRESS = {
    "Planning": 1,
    "Research": 1,
    "Dataset": 1,
    "Charting": 2,
    "Drafting": 2,
    "Building": 2,
    "Editing": 3,
    "Review": 3,
    "Ready": 4,
    "Publishing": 4,
    "Reference": 1,
}


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
            background-image: radial-gradient(
                circle,
                rgba(99, 213, 208, 0.16) 0.85px,
                transparent 1px
            );
            background-size: 22px 22px;
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

        .lost-nomad-title-accent {
            display: flex;
            align-items: center;
            width: 78px;
            height: 12px;
            margin: 0.6rem 0 0.65rem;
        }

        .lost-nomad-title-line {
            width: 58px;
            height: 2px;
            flex: 0 0 58px;
            background-color: var(--warm-turquoise);
            border-radius: 2px;
        }

        .lost-nomad-title-sun {
            width: 10px;
            height: 10px;
            flex: 0 0 10px;
            margin-left: -2px;
            box-sizing: border-box;
            background-color: var(--warm-pink);
            border: 2px solid var(--warm-background);
            border-radius: 50%;
            box-shadow: 0 0 0 3px rgba(247, 217, 122, 0.18);
        }

        .lost-nomad-title-segment {
            width: 8px;
            height: 2px;
            flex: 0 0 8px;
            margin-left: 4px;
            background-color: var(--warm-yellow);
            border-radius: 2px;
            opacity: 0.72;
        }

        .lost-nomad-title-accent.is-sidebar {
            width: 61px;
            height: 10px;
            margin: 0.45rem 0 0.5rem;
        }

        .lost-nomad-title-accent.is-sidebar .lost-nomad-title-line {
            width: 44px;
            flex-basis: 44px;
        }

        .lost-nomad-title-accent.is-sidebar .lost-nomad-title-sun {
            width: 8px;
            height: 8px;
            flex-basis: 8px;
            margin-left: -1px;
            border-width: 1px;
            border-color: var(--warm-surface);
            box-shadow: 0 0 0 2px rgba(247, 217, 122, 0.14);
        }

        .lost-nomad-title-accent.is-sidebar .lost-nomad-title-segment {
            width: 7px;
            flex-basis: 7px;
            margin-left: 3px;
        }

        .lost-nomad-title-accent.is-overview {
            width: 70px;
            margin: 0 0 0.4rem;
        }

        .lost-nomad-title-accent.is-overview .lost-nomad-title-line {
            width: 52px;
            flex-basis: 52px;
        }

        .lost-nomad-title-accent.is-overview .lost-nomad-title-segment {
            width: 6px;
            flex-basis: 6px;
        }

        .warm-command-center .lost-nomad-title-sun {
            border-color: var(--warm-surface);
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

        .warm-emoji-icon {
            font-family: "Segoe UI Emoji", "Apple Color Emoji", sans-serif;
            font-weight: 400;
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

        .warm-weekly-pulse {
            margin: 0 0 1.1rem;
            padding: 1rem 1.05rem 1.05rem;
            background-color: #FFFDFB;
            border: 1px solid var(--warm-border);
            border-radius: 8px;
            box-shadow: 0 5px 16px rgba(71, 56, 50, 0.055);
        }

        .warm-pulse-heading {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.75rem;
        }

        .warm-pulse-heading strong {
            display: block;
            color: var(--warm-text);
            font-size: 1rem;
            font-weight: 650;
        }

        .warm-pulse-heading span:last-child {
            color: var(--warm-muted);
            font-size: 0.8rem;
        }

        .warm-pulse-grid {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 0.6rem;
        }

        .warm-pulse-item {
            min-width: 0;
            padding: 0.7rem 0.75rem;
            background-color: var(--warm-background);
            border: 1px solid var(--warm-border);
            border-left: 4px solid var(--warm-gray);
            border-radius: 8px;
            box-shadow: 0 2px 7px rgba(71, 56, 50, 0.035);
        }

        .warm-pulse-item.is-active {
            background-color: #F4FCFB;
            border-color: #D7F1EE;
            border-left-color: var(--warm-turquoise);
        }

        .warm-pulse-item.is-open {
            background-color: #FFF7F9;
            border-color: #F5DDE3;
            border-left-color: var(--warm-pink);
        }

        .warm-pulse-item.is-overdue {
            background-color: #FFF8F7;
            border-color: #F6DEDB;
            border-left-color: var(--warm-coral);
        }

        .warm-pulse-item.is-upcoming {
            background-color: #FFFCF1;
            border-color: #F6EBC8;
            border-left-color: var(--warm-yellow);
        }

        .warm-pulse-item.is-ready {
            background-color: #F5FCF8;
            border-color: #D6EEE2;
            border-left-color: var(--warm-mint);
        }

        .warm-pulse-item.is-stale {
            background-color: #FAF8FE;
            border-color: #E5DFF6;
            border-left-color: var(--warm-lavender);
        }

        .warm-pulse-label {
            display: flex;
            align-items: center;
            gap: 0.35rem;
            min-height: 1.8rem;
            color: var(--warm-muted);
            font-size: 0.69rem;
            font-weight: 600;
            line-height: 1.2;
        }

        .warm-pulse-value {
            margin-top: 0.2rem;
            color: var(--warm-text);
            font-size: 1.82rem;
            font-weight: 700;
            line-height: 1.15;
        }

        .warm-pulse-detail {
            margin-top: 0.18rem;
            overflow: hidden;
            color: var(--warm-muted);
            font-size: 0.68rem;
            line-height: 1.25;
            text-overflow: ellipsis;
            white-space: nowrap;
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
            font-size: 1.55rem;
            font-weight: 700;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.75rem;
            font-weight: 600;
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
            margin: 0.35rem 0 0.7rem;
            box-sizing: border-box;
            background-color: var(--warm-surface);
            border: 1px solid var(--warm-border);
            border-radius: 8px;
            box-shadow: 0 3px 12px rgba(71, 56, 50, 0.04);
            font-size: 0.86rem;
        }

        [data-testid="stDataFrame"] [role="columnheader"],
        [data-testid="stDataFrame"] [role="gridcell"],
        [data-testid="stDataEditor"] [role="columnheader"],
        [data-testid="stDataEditor"] [role="gridcell"] {
            font-size: 0.84rem;
        }

        [data-testid="stDataFrame"] [data-testid="stElementToolbar"],
        [data-testid="stDataEditor"] [data-testid="stElementToolbar"] {
            margin: 0.2rem;
        }

        [data-testid="stDataFrame"] {
            border-top: 2px solid #BFEAE7;
        }

        [data-testid="stDataEditor"] {
            border-top: 2px solid #F2CDD6;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            padding: 1rem;
            margin: 0.45rem 0 1.05rem;
            background-color: var(--warm-surface);
            border-color: var(--warm-border) !important;
            border-radius: 8px;
            box-shadow: 0 3px 14px rgba(71, 56, 50, 0.045);
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.warm-future-section-header.is-turquoise) {
            background-color: #FBFEFD;
            border-left: 2px solid var(--warm-turquoise) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.warm-future-section-header.is-pink) {
            background-color: #FFFBFC;
            border-left: 2px solid var(--warm-pink) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.warm-future-section-header.is-yellow) {
            background-color: #FFFDF8;
            border-left: 2px solid var(--warm-yellow) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.warm-future-section-header.is-mint) {
            background-color: #FBFEFC;
            border-left: 2px solid var(--warm-mint) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.warm-future-section-header.is-lavender) {
            background-color: #FDFCFF;
            border-left: 2px solid var(--warm-lavender) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.warm-future-section-header.is-coral) {
            background-color: #FFFCFB;
            border-left: 2px solid var(--warm-coral) !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:has(.warm-future-section-header.is-gray) {
            background-color: #FDFCFB;
            border-left: 2px solid var(--warm-gray) !important;
        }

        .warm-future-section-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0.1rem 0 0.9rem;
            padding-left: 0.65rem;
            color: var(--warm-text);
            border-left: 4px solid var(--warm-turquoise);
            font-size: 1.2rem;
            font-weight: 600;
            line-height: 1.35;
        }

        .warm-future-section-header.is-pink {
            border-left-color: var(--warm-pink);
        }

        .warm-future-section-header.is-yellow {
            border-left-color: var(--warm-yellow);
        }

        .warm-future-section-header.is-mint {
            border-left-color: var(--warm-mint);
        }

        .warm-future-section-header.is-lavender {
            border-left-color: var(--warm-lavender);
        }

        .warm-future-section-header.is-coral {
            border-left-color: var(--warm-coral);
        }

        .warm-future-section-header.is-gray {
            border-left-color: var(--warm-gray);
        }

        .warm-future-section-icon {
            width: 1.35rem;
            flex: 0 0 1.35rem;
            font-size: 1rem;
            text-align: center;
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

        .warm-mini-stats {
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem 0.65rem;
            margin: 0 0 0.7rem;
            padding: 0.42rem 0.6rem;
            color: var(--warm-muted);
            background-color: rgba(255, 249, 244, 0.62);
            border: 1px solid var(--warm-border);
            border-radius: 6px;
            font-size: 0.72rem;
            line-height: 1.35;
        }

        .warm-mini-stat {
            display: inline-flex;
            align-items: baseline;
            gap: 0.22rem;
        }

        .warm-mini-stat strong {
            color: var(--warm-text);
            font-size: 0.78rem;
            font-weight: 700;
        }

        .warm-about-card {
            display: flex;
            align-items: flex-start;
            gap: 0.7rem;
            margin: 0.5rem 0 1rem;
            padding: 0.85rem 0.95rem;
            background-color: #FFFCF9;
            border: 1px solid var(--warm-border);
            border-left: 3px solid var(--warm-turquoise);
            border-radius: 8px;
            box-shadow: 0 3px 12px rgba(71, 56, 50, 0.04);
        }

        .warm-about-icon {
            font-size: 1rem;
            line-height: 1.3;
        }

        .warm-about-card strong {
            display: block;
            margin-bottom: 0.2rem;
            color: var(--warm-text);
            font-size: 0.82rem;
        }

        .warm-about-card p {
            margin: 0;
            color: var(--warm-muted);
            font-size: 0.78rem;
            line-height: 1.45;
        }

        .warm-project-progress {
            margin: 0.7rem 0 0.9rem;
            padding: 0.75rem 0.85rem;
            background-color: rgba(255, 249, 244, 0.72);
            border: 1px solid var(--warm-border);
            border-radius: 8px;
        }

        .warm-project-progress-heading {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 0.75rem;
            margin-bottom: 0.65rem;
        }

        .warm-project-progress-heading strong {
            color: var(--warm-text);
            font-size: 0.82rem;
            font-weight: 700;
        }

        .warm-project-progress-heading span {
            color: var(--warm-muted);
            font-size: 0.7rem;
        }

        .warm-project-progress-bar {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 4px;
        }

        .warm-project-progress-segment {
            height: 8px;
            background-color: #ECE5E0;
            border-radius: 4px;
        }

        .warm-project-progress-segment.is-filled {
            background-color: var(--warm-turquoise);
        }

        .warm-project-progress-segment.is-current {
            background-color: var(--warm-pink);
            box-shadow: 0 0 0 2px rgba(247, 217, 122, 0.3);
        }

        .warm-project-progress-scale {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            margin-top: 0.35rem;
            color: var(--warm-muted);
            font-size: 0.62rem;
        }

        .warm-project-progress-scale span {
            text-align: center;
        }

        .warm-project-progress-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.65rem;
        }

        .warm-project-progress-meta-item {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
        }

        .warm-project-progress-meta-label {
            color: var(--warm-muted);
            font-size: 0.66rem;
            font-weight: 600;
        }

        .warm-project-progress-value {
            display: inline-block;
            max-width: 100%;
            padding: 0.2rem 0.45rem;
            color: var(--warm-text);
            border: 1px solid var(--warm-border);
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            line-height: 1.25;
            overflow-wrap: anywhere;
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

            .warm-pulse-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (min-width: 701px) and (max-width: 1100px) {
            .warm-pulse-grid {
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }
        }

        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMetric"] {
            min-height: 96px;
            padding: 0.65rem 0.8rem;
            background-color: rgba(255, 249, 244, 0.72);
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
            padding: 0.95rem;
            background-color: #FFF9FA;
            border: 1px solid #EEDDE1;
            border-top: 3px solid var(--warm-turquoise);
            border-radius: 8px;
            box-shadow: 0 4px 14px rgba(71, 56, 50, 0.06);
        }

        .warm-sidebar-brand p.warm-sidebar-eyebrow {
            margin: 0 0 0.3rem;
            color: var(--warm-pink);
            font-size: 0.7rem;
            font-weight: 700;
        }

        .warm-sidebar-brand h2 {
            margin: 0;
            color: var(--warm-text);
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1.3;
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

        .warm-sidebar-nav-icon {
            display: inline-grid;
            width: 1.65rem;
            height: 1.65rem;
            flex: 0 0 1.65rem;
            place-items: center;
            border-radius: 6px;
            font-size: 0.88rem;
        }

        .warm-sidebar-nav-icon.is-projects {
            background-color: #FBE8ED;
        }

        .warm-sidebar-nav-icon.is-tasks {
            background-color: #E6F8F6;
        }

        .warm-sidebar-nav-icon.is-publishing {
            background-color: #EEEAFB;
        }

        .warm-sidebar-nav-icon.is-dashboard {
            background-color: #FFF6D8;
        }

        .warm-sidebar-meta-icon {
            display: inline-block;
            width: 1.15rem;
            margin-right: 0.25rem;
            text-align: center;
        }

        .warm-sidebar-meta,
        .warm-sidebar-workflow {
            margin-bottom: 0.8rem;
            padding: 0.8rem;
            background-color: var(--warm-background);
            border: 1px solid var(--warm-border);
            border-radius: 8px;
        }

        .warm-sidebar-meta {
            background-color: #F8FCFA;
            border-color: #D7EDE1;
            border-top: 3px solid var(--warm-mint);
            box-shadow: 0 3px 10px rgba(71, 56, 50, 0.035);
        }

        .warm-sidebar-workflow {
            background-color: #FFFDF5;
            border-color: #EFE5C4;
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

        .warm-sidebar-legend {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.35rem 0.45rem;
            margin-bottom: 0.8rem;
            padding: 0.7rem;
            background-color: var(--warm-background);
            border: 1px solid var(--warm-border);
            border-radius: 8px;
        }

        .warm-sidebar-legend-item {
            display: flex;
            align-items: center;
            min-width: 0;
            gap: 0.35rem;
            color: var(--warm-muted);
            font-size: 0.68rem;
            line-height: 1.25;
        }

        .warm-sidebar-legend-dot {
            width: 8px;
            height: 8px;
            flex: 0 0 8px;
            background-color: var(--warm-gray);
            border-radius: 50%;
        }

        .warm-sidebar-legend-dot.is-active {
            background-color: var(--warm-turquoise);
        }

        .warm-sidebar-legend-dot.is-ready,
        .warm-sidebar-legend-dot.is-published {
            background-color: var(--warm-mint);
        }

        .warm-sidebar-legend-dot.is-blocked {
            background-color: var(--warm-coral);
        }

        .warm-sidebar-legend-dot.is-reference {
            background-color: var(--warm-yellow);
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

        .warm-footer {
            margin-top: 1.8rem;
            padding: 1rem 0 0.55rem;
            color: var(--warm-muted);
            border-top: 1px solid var(--warm-border);
            font-size: 0.74rem;
            line-height: 1.45;
            text-align: center;
        }

        .warm-footer strong {
            color: var(--warm-text);
            font-weight: 600;
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
            <div class="lost-nomad-title-accent" aria-hidden="true">
                <span class="lost-nomad-title-line"></span>
                <span class="lost-nomad-title-sun"></span>
                <span class="lost-nomad-title-segment"></span>
            </div>
            <p class="warm-future-subtitle">{safe_subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(last_refreshed):
    safe_last_refreshed = escape(last_refreshed)

    st.sidebar.markdown(
        f"""
        <div class="warm-sidebar-brand">
            <p class="warm-sidebar-eyebrow">LOST NOMAD</p>
            <h2>Project Dashboard</h2>
            <div class="lost-nomad-title-accent is-sidebar" aria-hidden="true">
                <span class="lost-nomad-title-line"></span>
                <span class="lost-nomad-title-sun"></span>
                <span class="lost-nomad-title-segment"></span>
            </div>
            <p>Personal command center</p>
        </div>

        <p class="warm-sidebar-label">MAIN SECTIONS</p>
        <div class="warm-sidebar-nav" aria-label="Main sections">
            <div class="warm-sidebar-nav-item">
                <span class="warm-sidebar-nav-icon warm-emoji-icon is-projects">📁</span>Projects
            </div>
            <div class="warm-sidebar-nav-item">
                <span class="warm-sidebar-nav-icon warm-emoji-icon is-tasks">✅</span>Tasks
            </div>
            <div class="warm-sidebar-nav-item">
                <span class="warm-sidebar-nav-icon warm-emoji-icon is-publishing">📰</span>Publishing Queue
            </div>
            <div class="warm-sidebar-nav-item">
                <span class="warm-sidebar-nav-icon warm-emoji-icon is-dashboard">📊</span>Dashboard
            </div>
        </div>

        <p class="warm-sidebar-label">APP STATUS</p>
        <div class="warm-sidebar-meta">
            <div class="warm-sidebar-meta-row">
                <span><span class="warm-sidebar-meta-icon warm-emoji-icon">🗂️</span>Data source</span>
                <strong>Google Sheets</strong>
            </div>
            <div class="warm-sidebar-meta-row">
                <span><span class="warm-sidebar-meta-icon warm-emoji-icon">🔗</span>Storage</span>
                <span class="warm-sidebar-connected">Connected</span>
            </div>
            <div class="warm-sidebar-meta-row">
                <span><span class="warm-sidebar-meta-icon warm-emoji-icon">🕒</span>Last refreshed</span>
                <strong>{safe_last_refreshed}</strong>
            </div>
        </div>

        <p class="warm-sidebar-label">STATUS LEGEND</p>
        <div class="warm-sidebar-legend" aria-label="Status color legend">
            <span class="warm-sidebar-legend-item">
                <span class="warm-sidebar-legend-dot is-active"></span>Active
            </span>
            <span class="warm-sidebar-legend-item">
                <span class="warm-sidebar-legend-dot"></span>Paused
            </span>
            <span class="warm-sidebar-legend-item">
                <span class="warm-sidebar-legend-dot is-ready"></span>Ready
            </span>
            <span class="warm-sidebar-legend-item">
                <span class="warm-sidebar-legend-dot is-published"></span>Published
            </span>
            <span class="warm-sidebar-legend-item">
                <span class="warm-sidebar-legend-dot is-blocked"></span>Blocked / overdue
            </span>
            <span class="warm-sidebar-legend-item">
                <span class="warm-sidebar-legend-dot is-reference"></span>Reference
            </span>
        </div>

        <p class="warm-sidebar-label">WORKFLOW</p>
        <div class="warm-sidebar-workflow">
            <p>Plan <span>&rarr;</span> Build <span>&rarr;</span> Publish <span>&rarr;</span> Review</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="warm-footer">
            <strong>Lost Nomad</strong> &middot; Warm Future workspace &middot;
            Built with Streamlit + Google Sheets
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard_hero():
    st.markdown(
        """
        <div class="warm-command-center">
            <div>
                <div class="lost-nomad-title-accent is-overview" aria-hidden="true">
                    <span class="lost-nomad-title-line"></span>
                    <span class="lost-nomad-title-sun"></span>
                    <span class="lost-nomad-title-segment"></span>
                </div>
                <h2><span class="warm-emoji-icon">📊</span> Lost Nomad Project Command Center</h2>
                <p>Tracking projects, publishing, and optimistic futures.</p>
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


def render_weekly_pulse(
    active_projects,
    open_tasks,
    high_priority_tasks,
    overdue_tasks,
    upcoming_deadlines,
    ready_outputs,
    stale_projects,
):
    overdue_detail = "All clear" if overdue_tasks == 0 else "Worth a look"
    stale_detail = "No drift" if stale_projects == 0 else "Could use a nudge"

    pulse_items = [
        ("📁", "Active projects", active_projects, "In motion", "active"),
        (
            "✅",
            "Open tasks",
            open_tasks,
            f"{high_priority_tasks} high priority",
            "open",
        ),
        ("🚨", "Overdue", overdue_tasks, overdue_detail, "overdue"),
        ("⏰", "Coming up", upcoming_deadlines, "On the horizon", "upcoming"),
        ("📝", "Ready to publish", ready_outputs, "Good to go", "ready"),
        ("🕒", "Stale projects", stale_projects, stale_detail, "stale"),
    ]

    item_markup = "".join(
        f"""
        <div class="warm-pulse-item is-{tone}">
            <div class="warm-pulse-label">
                <span class="warm-emoji-icon">{icon}</span>{label}
            </div>
            <div class="warm-pulse-value">{value}</div>
            <div class="warm-pulse-detail">{detail}</div>
        </div>
        """
        for icon, label, value, detail, tone in pulse_items
    )

    st.markdown(
        f"""
        <div class="warm-weekly-pulse">
            <div class="warm-pulse-heading">
                <span class="warm-emoji-icon">📈</span>
                <div>
                    <strong>Weekly Pulse</strong>
                    <span>A quick read on how things are moving.</span>
                </div>
            </div>
            <div class="warm-pulse-grid">{item_markup}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_card(title, icon=None, tone="turquoise"):
    card = st.container(border=True)
    icon_markup = ""
    if icon:
        icon_markup = (
            '<span class="warm-future-section-icon warm-emoji-icon">'
            f"{escape(icon)}</span>"
        )

    allowed_tones = {
        "turquoise",
        "pink",
        "yellow",
        "mint",
        "lavender",
        "coral",
        "gray",
    }
    safe_tone = tone if tone in allowed_tones else "turquoise"

    card.markdown(
        f'<div class="warm-future-section-header is-{safe_tone}">'
        f"{icon_markup}<span>{escape(title)}</span></div>",
        unsafe_allow_html=True,
    )
    return card


def render_empty_state(container, message):
    container.markdown(
        f'<div class="warm-empty-state">{escape(message)}</div>',
        unsafe_allow_html=True,
    )


def render_mini_stats(container, items):
    stat_markup = "".join(
        f'<span class="warm-mini-stat"><strong>{count}</strong>{escape(label)}</span>'
        for count, label in items
    )
    container.markdown(
        f'<div class="warm-mini-stats">{stat_markup}</div>',
        unsafe_allow_html=True,
    )


def render_about_dashboard():
    st.markdown(
        """
        <div class="warm-about-card">
            <span class="warm-about-icon warm-emoji-icon">🧭</span>
            <div>
                <strong>About this dashboard</strong>
                <p>Built to track projects, publishing, research, and experiments
                across the Lost Nomad ecosystem.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_project_progress(container, status, stage):
    status_background, status_border = STATUS_BADGE_STYLES.get(
        status,
        DEFAULT_STATUS_BADGE_STYLE,
    )
    stage_background, stage_border = STAGE_BADGE_STYLES.get(
        stage,
        DEFAULT_STAGE_BADGE_STYLE,
    )
    progress_step = max(
        PROJECT_STATUS_PROGRESS.get(status, 1),
        PROJECT_STAGE_PROGRESS.get(stage, 1),
    )
    segment_markup = "".join(
        '<span class="warm-project-progress-segment'
        f"{' is-filled' if step <= progress_step else ''}"
        f"{' is-current' if step == progress_step else ''}"
        '"></span>'
        for step in range(1, 5)
    )

    container.markdown(
        f"""
        <div class="warm-project-progress">
            <div class="warm-project-progress-heading">
                <strong>Project Progress</strong>
                <span>Qualitative movement</span>
            </div>
            <div class="warm-project-progress-bar" aria-label="Qualitative project progress">
                {segment_markup}
            </div>
            <div class="warm-project-progress-scale" aria-hidden="true">
                <span>Plan</span><span>Build</span><span>Review</span><span>Ready</span>
            </div>
            <div class="warm-project-progress-meta">
                <div class="warm-project-progress-meta-item">
                    <span class="warm-project-progress-meta-label">Status</span>
                    <span class="warm-project-progress-value"
                        style="background-color: {status_background}; border-color: {status_border};">
                        {escape(str(status))}
                    </span>
                </div>
                <div class="warm-project-progress-meta-item">
                    <span class="warm-project-progress-meta-label">Stage</span>
                    <span class="warm-project-progress-value"
                        style="background-color: {stage_background}; border-color: {stage_border};">
                        {escape(str(stage))}
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_table_indicators(dataframe):
    indicator_columns = {"Status", "Stage", "Priority"}
    if not indicator_columns.intersection(dataframe.columns):
        return dataframe

    def indicator_style(value, styles, default_style):
        background, border = styles.get(
            value,
            default_style,
        )

        return (
            f"background-color: {background}; "
            f"border: 1px solid {border}; "
            "color: #2F2A28; "
            "font-weight: 600; "
            "text-align: center; "
            "border-radius: 6px;"
        )

    styled = dataframe.style

    if "Status" in dataframe.columns:
        styled = styled.apply(
            lambda values: [
                indicator_style(value, STATUS_BADGE_STYLES, DEFAULT_STATUS_BADGE_STYLE)
                for value in values
            ],
            subset=["Status"],
        )

    if "Stage" in dataframe.columns:
        styled = styled.apply(
            lambda values: [
                indicator_style(value, STAGE_BADGE_STYLES, DEFAULT_STAGE_BADGE_STYLE)
                for value in values
            ],
            subset=["Stage"],
        )

    if "Priority" in dataframe.columns:
        styled = styled.apply(
            lambda values: [
                (
                    "background-color: #FFF2F5; "
                    "border-left: 3px solid #E56B8A; "
                    "color: #2F2A28; font-weight: 700;"
                    if value == "High"
                    else ""
                )
                for value in values
            ],
            subset=["Priority"],
        )

    return styled
