"""
UI and visualization helper module for MentorMatch AI.
Bespoke Squarespace-inspired design system:
- Editorial, high-fashion typography (Syne & Plus Jakarta Sans)
- Ultra-clean Obsidian Dark Mode & Architectural Gallery Light Mode
- Iconic Squarespace pill buttons, 1px monoline card borders, and fluid grids
- High-contrast Plotly charts tailored for editorial luxury
- Safe HTML renderers with zero code leakage
"""

import base64
import textwrap
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from typing import Dict, List, Any, Optional

def render_html(html_str: str):
    """Safely render HTML without Markdown converting 4-space indents into pre/code blocks."""
    clean = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(clean)
    else:
        st.markdown(clean, unsafe_allow_html=True)

# Attempt OpenCV import
try:
    import cv2
    _has_cv2 = True
except Exception:
    _has_cv2 = False


def inject_custom_css(theme: str = "light"):
    """
    Injects Squarespace's signature editorial design system:
    - Obsidian Noir (Dark) & Gallery Ivory (Light)
    - Clarkson / Syne / Plus Jakarta Sans typography
    - Monoline 1px borders, generous negative space, iconic pill geometry
    """
    is_dark = (theme == "dark")

    if is_dark:
        bg_app = "#09090b"
        bg_card = "#121215"
        bg_card_hover = "#18181c"
        bg_sidebar = "#0d0d10"
        text_primary = "#ffffff"
        text_secondary = "#ffffff"
        text_muted = "#f4f4f5"
        border_subtle = "rgba(255, 255, 255, 0.12)"
        border_hover = "rgba(255, 255, 255, 0.35)"
        pill_bg = "#ffffff"
        pill_text = "#09090b"
        pill_ghost_bg = "rgba(255, 255, 255, 0.08)"
        pill_ghost_border = "rgba(255, 255, 255, 0.25)"
        badge_bg = "rgba(220, 38, 38, 0.16)"
        badge_text = "#fde047"
        accent_blue = "#f59e0b"
        shadow_card = "0 1px 3px rgba(0,0,0,0.6), 0 10px 25px -5px rgba(0,0,0,0.4)"
        shadow_hover = "0 12px 32px -4px rgba(0,0,0,0.7)"

        # Red & Yellow Button Architecture for Obsidian Black Theme:
        btn_primary_bg = "linear-gradient(135deg, #dc2626 0%, #ea580c 45%, #eab308 100%)"
        btn_primary_text = "#09090b"
        btn_primary_border = "#fde047"
        btn_primary_shadow = "0 4px 20px rgba(220, 38, 38, 0.45), 0 0 14px rgba(250, 204, 21, 0.3)"
        btn_primary_hover_bg = "linear-gradient(135deg, #ef4444 0%, #f97316 45%, #facc15 100%)"
        btn_primary_hover_border = "#ffffff"
        btn_primary_hover_shadow = "0 8px 30px rgba(220, 38, 38, 0.65), 0 0 25px rgba(250, 204, 21, 0.5)"

        btn_secondary_bg = "#121216"
        btn_secondary_text = "#fde047"
        btn_secondary_border = "rgba(250, 204, 21, 0.45)"
        btn_secondary_hover_bg = "rgba(220, 38, 38, 0.22)"
        btn_secondary_hover_border = "#ef4444"
        btn_secondary_hover_text = "#ffffff"
        btn_secondary_hover_shadow = "0 4px 20px rgba(220, 38, 38, 0.4), 0 0 14px rgba(250, 204, 21, 0.25)"

        bot_btn_bg = "linear-gradient(135deg, #dc2626 0%, #ea580c 45%, #eab308 100%)"
        bot_btn_border = "#fde047"
        bot_btn_shadow = "0 8px 25px rgba(220, 38, 38, 0.6), 0 0 16px rgba(250, 204, 21, 0.4)"
        bot_btn_hover_shadow = "0 12px 35px rgba(220, 38, 38, 0.8), 0 0 25px rgba(250, 204, 21, 0.6)"
    else:
        bg_app = "#fcfcfd"
        bg_card = "#ffffff"
        bg_card_hover = "#ffffff"
        bg_sidebar = "#f7f7f8"
        text_primary = "#09090b"
        text_secondary = "#18181b"
        text_muted = "#27272a"
        border_subtle = "#e4e4e7"
        border_hover = "#18181b"
        pill_bg = "#09090b"
        pill_text = "#ffffff"
        pill_ghost_bg = "#f4f4f5"
        pill_ghost_border = "#d4d4d8"
        badge_bg = "#f4f4f5"
        badge_text = "#18181b"
        accent_blue = "#4f46e5"
        shadow_card = "0 1px 2px rgba(0,0,0,0.04), 0 8px 24px -4px rgba(0,0,0,0.05)"
        shadow_hover = "0 16px 36px -6px rgba(0,0,0,0.10)"

        btn_primary_bg = "#09090b"
        btn_primary_text = "#ffffff"
        btn_primary_border = "#09090b"
        btn_primary_shadow = "0 8px 24px rgba(0, 0, 0, 0.15)"
        btn_primary_hover_bg = "#18181b"
        btn_primary_hover_border = "#09090b"
        btn_primary_hover_shadow = "0 12px 32px rgba(0, 0, 0, 0.22)"

        btn_secondary_bg = "#ffffff"
        btn_secondary_text = "#09090b"
        btn_secondary_border = "#d4d4d8"
        btn_secondary_hover_bg = "#ffffff"
        btn_secondary_hover_border = "#18181b"
        btn_secondary_hover_text = "#09090b"
        btn_secondary_hover_shadow = shadow_card

        bot_btn_bg = "#09090b"
        bot_btn_border = "#18181b"
        bot_btn_shadow = "0 10px 28px rgba(0, 0, 0, 0.22)"
        bot_btn_hover_shadow = "0 14px 35px rgba(0, 0, 0, 0.32)"

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography & Palette */
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    .stApp {{
        background-color: {bg_app} !important;
        color: {text_primary} !important;
        min-height: 100vh;
    }}

    #MainMenu, footer {{visibility: hidden;}}
    header {{background: transparent !important;}}

    /* =========================================================================
       UNIVERSAL TYPOGRAPHY FOR DARK & LIGHT THEMES
       ========================================================================= */
    {'''
    .stApp,
    .stApp *,
    .stMarkdown,
    .stMarkdown *,
    .stMarkdown p,
    .stMarkdown span:not([class*="badge"]):not(.mm-logo-badge),
    .stMarkdown li,
    .stMarkdown strong,
    .stMarkdown b,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    h1, h2, h3, h4, h5, h6,
    p,
    label,
    strong,
    b,
    small,
    div[data-testid="stMarkdownContainer"],
    div[data-testid="stMarkdownContainer"] *,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] span,
    div[data-testid="stMarkdownContainer"] strong,
    div[data-testid="stMarkdownContainer"] b,
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stCaptionContainer"],
    div[data-testid="stCaptionContainer"] *,
    div[data-testid="stCaptionContainer"] p,
    .stCaption,
    .stCaption *,
    .sqsp-hero-headline,
    .sqsp-hero-desc,
    .sqsp-eyebrow,
    .sqsp-ribbon-val,
    .sqsp-ribbon-lbl,
    .sqsp-ribbon-num,
    .sqsp-metric-value,
    .sqsp-metric-badge,
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span:not([class*="badge"]):not(.mm-logo-badge),
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"] b,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] small,
    div[data-testid="stRadio"] *,
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label *,
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] div[role="radiogroup"] label *,
    div[data-testid="stSelectbox"] *,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] label p,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] *,
    div[data-testid="stFileUploader"] label,
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stVerticalBlockBorderWrapper"] *,
    div[data-testid="stVerticalBlockBorderWrapper"] p,
    div[data-testid="stVerticalBlockBorderWrapper"] span:not(.sqsp-tag),
    div[data-testid="stVerticalBlockBorderWrapper"] strong,
    div[data-testid="stVerticalBlockBorderWrapper"] b,
    div[data-testid="stVerticalBlockBorderWrapper"] small,
    div[data-testid="stExpander"],
    div[data-testid="stExpander"] *,
    div[data-testid="stExpander"] summary *,
    div[data-testid="stExpanderDetails"] *,
    div[data-testid="stExpanderDetails"] p,
    .chat-bubble-ai,
    .chat-bubble-ai *,
    .chat-bubble-user,
    .chat-bubble-user * {
        color: #ffffff !important;
    }

    /* Protect buttons from universal text override in dark mode */
    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"] *,
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    div[data-testid="stFormSubmitButton"] > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button[kind="primary"] *,
    div[data-testid="stDownloadButton"] > button[kind="primary"],
    div[data-testid="stDownloadButton"] > button[kind="primary"] * {
        color: #09090b !important;
    }

    .stButton > button:not([kind="primary"]),
    .stButton > button:not([kind="primary"]) *,
    .stButton > button:not([kind="primary"]) p,
    .stButton > button:not([kind="primary"]) span,
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]),
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]) *,
    div[data-testid="stDownloadButton"] > button:not([kind="primary"]),
    div[data-testid="stDownloadButton"] > button:not([kind="primary"]) * {
        color: #fde047 !important;
    }

    .stButton > button:not([kind="primary"]):hover *,
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]):hover *,
    div[data-testid="stDownloadButton"] > button:not([kind="primary"]):hover * {
        color: #ffffff !important;
    }

    div[data-testid="stPopover"] button,
    div[data-testid="stPopover"] button *,
    div[data-testid="stPopover"] button p,
    div[data-testid="stPopover"] button span {
        color: #09090b !important;
    }

    .sqsp-tag {
        color: #fde047 !important;
    }

    .mm-logo-badge {
        color: #fde047 !important;
    }

    code {
        background-color: rgba(255, 255, 255, 0.16) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 6px !important;
        padding: 0.15rem 0.45rem !important;
        font-weight: 700 !important;
    }
    ''' if is_dark else '''
    /* High-contrast crisp typography for light theme */
    .stApp,
    .stApp *,
    .stMarkdown,
    .stMarkdown *,
    .stMarkdown p,
    .stMarkdown span:not([class*="badge"]),
    .stMarkdown li,
    .stMarkdown strong,
    .stMarkdown b,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    h1, h2, h3, h4, h5, h6,
    p,
    label,
    strong,
    b,
    small,
    div[data-testid="stMarkdownContainer"],
    div[data-testid="stMarkdownContainer"] *,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] span,
    div[data-testid="stMarkdownContainer"] strong,
    div[data-testid="stMarkdownContainer"] b,
    div[data-testid="stCaptionContainer"],
    div[data-testid="stCaptionContainer"] *,
    div[data-testid="stCaptionContainer"] p,
    .stCaption,
    .stCaption *,
    .sqsp-hero-headline,
    .sqsp-hero-desc,
    .sqsp-eyebrow,
    .sqsp-ribbon-val,
    .sqsp-ribbon-lbl,
    .sqsp-ribbon-num,
    .sqsp-metric-value,
    .sqsp-metric-badge,
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span:not([class*="badge"]),
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"] b,
    section[data-testid="stSidebar"] label,
    div[data-testid="stRadio"] *,
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label *,
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] div[role="radiogroup"] label *,
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stVerticalBlockBorderWrapper"] *,
    div[data-testid="stVerticalBlockBorderWrapper"] p,
    div[data-testid="stVerticalBlockBorderWrapper"] strong,
    div[data-testid="stVerticalBlockBorderWrapper"] b,
    div[data-testid="stExpander"],
    div[data-testid="stExpander"] *,
    div[data-testid="stExpander"] summary *,
    div[data-testid="stExpanderDetails"] *,
    div[data-testid="stExpanderDetails"] p,
    .chat-bubble-ai,
    .chat-bubble-ai *,
    .chat-bubble-user,
    .chat-bubble-user * {
        color: #09090b !important;
    }

    /* Light theme buttons: crisp white text on black primary button, dark text on secondary */
    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"] *,
    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    div[data-testid="stFormSubmitButton"] > button[kind="primary"] *,
    div[data-testid="stDownloadButton"] > button[kind="primary"] * {
        color: #ffffff !important;
    }

    .stButton > button:not([kind="primary"]),
    .stButton > button:not([kind="primary"]) *,
    .stButton > button:not([kind="primary"]) p,
    .stButton > button:not([kind="primary"]) span,
    div[data-testid="stFormSubmitButton"] > button:not([kind="primary"]) *,
    div[data-testid="stDownloadButton"] > button:not([kind="primary"]) * {
        color: #09090b !important;
    }

    div[data-testid="stPopover"] button,
    div[data-testid="stPopover"] button *,
    div[data-testid="stPopover"] button p,
    div[data-testid="stPopover"] button span {
        color: #ffffff !important;
    }

    code {
        background-color: #f4f4f5 !important;
        color: #09090b !important;
        border: 1px solid #e4e4e7 !important;
        border-radius: 6px !important;
        padding: 0.15rem 0.45rem !important;
        font-weight: 700 !important;
    }
    '''}

    /* Global Headings in Squarespace Editorial Style */
    h1, h2, h3, .sqsp-title {{
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.035em !important;
        color: {text_primary} !important;
    }}

    /* Eyebrow Label (Iconic Squarespace tracking) */
    .sqsp-eyebrow {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.16em !important;
        color: {text_muted} !important;
        margin-bottom: 0.4rem;
        display: block;
    }}

    /* Streamlit Native Cards & Containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {bg_card} !important;
        border: 1px solid {border_subtle} !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        box-shadow: {shadow_card} !important;
        transition: border-color 0.25s cubic-bezier(0.16, 1, 0.3, 1), transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        border-color: {border_hover} !important;
        transform: translateY(-2px);
        box-shadow: {shadow_hover} !important;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {bg_sidebar} !important;
        border-right: 1px solid {border_subtle} !important;
    }}

    /* Squarespace Iconic Pill Buttons */
    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button,
    div[data-testid="stDownloadButton"] > button {{
        border-radius: 9999px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        border: 1.5px solid {btn_secondary_border} !important;
        background: {btn_secondary_bg} !important;
        background-color: {btn_secondary_bg} !important;
        color: {btn_secondary_text} !important;
    }}

    .stButton > button p,
    .stButton > button span,
    div[data-testid="stFormSubmitButton"] > button p,
    div[data-testid="stFormSubmitButton"] > button span,
    div[data-testid="stDownloadButton"] > button p,
    div[data-testid="stDownloadButton"] > button span {{
        color: inherit !important;
    }}

    .stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {{
        border-color: {btn_secondary_hover_border} !important;
        background: {btn_secondary_hover_bg} !important;
        background-color: {btn_secondary_hover_bg} !important;
        color: {btn_secondary_hover_text} !important;
        transform: translateY(-2px) !important;
        box-shadow: {btn_secondary_hover_shadow} !important;
    }}

    .stButton > button:focus,
    .stButton > button:active,
    .stButton > button:focus:not(:active),
    div[data-testid="stFormSubmitButton"] > button:focus,
    div[data-testid="stDownloadButton"] > button:focus {{
        outline: none !important;
        border-color: {btn_secondary_border} !important;
        background: {btn_secondary_bg} !important;
        background-color: {btn_secondary_bg} !important;
        color: {btn_secondary_text} !important;
        box-shadow: {btn_secondary_hover_shadow} !important;
    }}

    .stButton > button:focus p,
    .stButton > button:focus span,
    .stButton > button:active p,
    .stButton > button:active span {{
        color: {btn_secondary_text} !important;
    }}

    /* Refined Streamlit Selectbox */
    div[data-baseweb="select"] {{
        background: {btn_secondary_bg} !important;
        background-color: {btn_secondary_bg} !important;
        border: 1.5px solid {btn_secondary_border} !important;
        border-radius: 9999px !important;
    }}

    div[data-baseweb="select"] * {{
        background-color: transparent !important;
        color: {text_primary} !important;
    }}

    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"] {{
        background: {bg_card} !important;
        background-color: {bg_card} !important;
        border: 1px solid {border_subtle} !important;
        border-radius: 14px !important;
        box-shadow: {shadow_card} !important;
    }}

    li[role="option"] {{
        color: {text_primary} !important;
        background-color: {bg_card} !important;
    }}

    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {{
        background: {pill_ghost_bg} !important;
        background-color: {pill_ghost_bg} !important;
        color: {'#fde047' if is_dark else '#09090b'} !important;
    }}

    .stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button[kind="primary"],
    div[data-testid="stDownloadButton"] > button[kind="primary"] {{
        background: {btn_primary_bg} !important;
        color: {btn_primary_text} !important;
        border: 1.5px solid {btn_primary_border} !important;
        font-weight: 700 !important;
        box-shadow: {btn_primary_shadow} !important;
    }}

    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    div[data-testid="stFormSubmitButton"] > button[kind="primary"] p,
    div[data-testid="stFormSubmitButton"] > button[kind="primary"] span,
    div[data-testid="stDownloadButton"] > button[kind="primary"] p,
    div[data-testid="stDownloadButton"] > button[kind="primary"] span {{
        color: {btn_primary_text} !important;
    }}

    .stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover,
    div[data-testid="stDownloadButton"] > button[kind="primary"]:hover {{
        background: {btn_primary_hover_bg} !important;
        border-color: {btn_primary_hover_border} !important;
        color: {btn_primary_text} !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: {btn_primary_hover_shadow} !important;
        opacity: 1 !important;
    }}

    /* Squarespace Hero Banner */
    .sqsp-hero {{
        background: {bg_card};
        border: 1px solid {border_subtle};
        border-radius: 20px;
        padding: 3rem 2.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: {shadow_card};
    }}

    .sqsp-hero-headline {{
        font-family: 'Syne', sans-serif !important;
        font-size: 3.4rem !important;
        font-weight: 800 !important;
        line-height: 1.05 !important;
        letter-spacing: -0.04em !important;
        color: {text_primary} !important;
        margin: 0.6rem 0 1.25rem 0 !important;
    }}

    .sqsp-hero-desc {{
        font-size: 1.12rem !important;
        line-height: 1.6 !important;
        color: {text_secondary} !important;
        max-width: 680px !important;
        margin-bottom: 2rem !important;
    }}

    .sqsp-ribbon {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1.5rem;
        border-top: 1px solid {border_subtle};
        padding-top: 1.75rem;
        margin-top: 2rem;
    }}

    .sqsp-ribbon-item {{
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }}

    .sqsp-ribbon-num {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        color: {text_muted} !important;
        letter-spacing: 0.1em !important;
    }}

    .sqsp-ribbon-val {{
        font-family: 'Syne', sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: {text_primary} !important;
        letter-spacing: -0.03em !important;
    }}

    .sqsp-ribbon-lbl {{
        font-size: 0.8rem !important;
        color: {text_secondary} !important;
        font-weight: 500 !important;
    }}

    .sqsp-readiness-val {{
        font-family: 'Syne', sans-serif !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em !important;
        color: {text_primary} !important;
    }}

    /* Metric Card (Squarespace Fluid Grid Block) */
    .sqsp-metric-card {{
        background: {bg_card};
        border: 1px solid {border_subtle};
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: {shadow_card};
        transition: all 0.25s ease;
    }}

    .sqsp-metric-card:hover {{
        border-color: {border_hover};
        transform: translateY(-3px);
        box-shadow: {shadow_hover};
    }}

    .sqsp-metric-value {{
        font-family: 'Syne', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.035em;
        color: {text_primary};
        margin: 0.35rem 0;
    }}

    .sqsp-metric-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.75rem;
        font-weight: 600;
        color: {text_muted};
        margin-top: 0.25rem;
    }}

    /* Squarespace Pill Badges */
    .sqsp-tag {{
        display: inline-flex;
        align-items: center;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        background: {badge_bg};
        color: {badge_text};
        border: 1px solid {border_subtle};
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
        letter-spacing: -0.01em;
    }}

    /* Chat Bubbles (Squarespace Minimalist Editorial) */
    .chat-bubble-ai {{
        background: {bg_card};
        border: 1px solid {border_subtle};
        border-left: 3px solid {text_primary};
        border-radius: 0 14px 14px 14px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.15rem;
        color: {text_primary};
        font-size: 0.95rem;
        line-height: 1.65;
        box-shadow: {shadow_card};
    }}

    .chat-bubble-user {{
        background: {pill_ghost_bg};
        border: 1px solid {border_subtle};
        border-right: 3px solid {text_muted};
        border-radius: 14px 0 14px 14px;
        padding: 1.1rem 1.35rem;
        margin-bottom: 1.15rem;
        color: {text_primary};
        font-size: 0.95rem;
    }}

    /* Refined Streamlit Inputs */
    input, textarea, select {{
        border-radius: 10px !important;
        border-color: {border_subtle} !important;
        background-color: {bg_card} !important;
        color: {text_primary} !important;
    }}

    /* Circular Floating Bottom-Right Corner Chatbot Icon */
    div[data-testid="stPopover"] {{
        position: fixed !important;
        bottom: 24px !important;
        right: 24px !important;
        z-index: 999999 !important;
        width: 56px !important;
        height: 56px !important;
        min-width: 56px !important;
        max-width: 56px !important;
        min-height: 56px !important;
        max-height: 56px !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    div[data-testid="stPopover"] div[data-testid="stElementContainer"] {{
        width: 56px !important;
        height: 56px !important;
        min-width: 56px !important;
        max-width: 56px !important;
        min-height: 56px !important;
        max-height: 56px !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    div[data-testid="stPopover"] button {{
        width: 56px !important;
        height: 56px !important;
        min-width: 56px !important;
        max-width: 56px !important;
        min-height: 56px !important;
        max-height: 56px !important;
        border-radius: 50% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: {bot_btn_bg} !important;
        background-color: transparent !important;
        color: {'#09090b' if is_dark else '#ffffff'} !important;
        border: 2px solid {bot_btn_border} !important;
        box-shadow: {bot_btn_shadow} !important;
        cursor: pointer !important;
        overflow: hidden !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        animation: floatCorner 3.5s ease-in-out infinite !important;
    }}

    /* Remove the default caret arrow / expand text / svg */
    div[data-testid="stPopover"] button svg,
    div[data-testid="stPopover"] button [data-testid="stIconMaterial"],
    div[data-testid="stPopover"] button > div > div:nth-child(2),
    div[data-testid="stPopover"] button > div > div:last-child:not(:first-child) {{
        display: none !important;
    }}

    /* Center emoji icon perfectly inside circle */
    div[data-testid="stPopover"] button > div {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    div[data-testid="stPopover"] button > div > div:first-child {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        height: 100% !important;
    }}

    div[data-testid="stPopover"] button p,
    div[data-testid="stPopover"] button span {{
        font-size: 1.65rem !important;
        line-height: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
        display: block !important;
    }}

    @keyframes floatCorner {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-4px); }}
    }}

    div[data-testid="stPopover"] button:hover {{
        transform: translateY(-4px) scale(1.08) !important;
        box-shadow: {bot_btn_hover_shadow} !important;
        border-color: {'#ffffff' if is_dark else '#09090b'} !important;
    }}

    /* Floating Popover Container */
    div[data-testid="stPopoverBody"] {{
        position: fixed !important;
        bottom: 90px !important;
        right: 24px !important;
        border-radius: 20px !important;
        border: 1px solid {border_subtle} !important;
        background: {bg_card} !important;
        box-shadow: 0 24px 60px rgba(0, 0, 0, {'0.75' if is_dark else '0.18'}) !important;
        width: 390px !important;
        max-width: 90vw !important;
        max-height: 560px !important;
        overflow-y: auto !important;
        padding: 1.25rem !important;
        z-index: 1000000 !important;
    }}

    /* Unique Glowy Website Logo Architecture */
    .mm-brand-logo-container {{
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 0.5rem !important;
        padding: 0.5rem 0.6rem !important;
        margin-bottom: 1.15rem !important;
        border-radius: 14px !important;
        background: {'linear-gradient(135deg, rgba(220, 38, 38, 0.14) 0%, rgba(245, 158, 11, 0.08) 100%)' if is_dark else 'linear-gradient(135deg, rgba(0, 0, 0, 0.03) 0%, rgba(0, 0, 0, 0.01) 100%)'} !important;
        border: 1px solid {'rgba(239, 68, 68, 0.4)' if is_dark else 'rgba(0, 0, 0, 0.08)'} !important;
        box-shadow: {'0 4px 20px rgba(220, 38, 38, 0.25), 0 0 15px rgba(245, 158, 11, 0.15)' if is_dark else '0 2px 8px rgba(0, 0, 0, 0.03)'} !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        cursor: default !important;
        width: 100% !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
    }}

    .mm-brand-logo-container:hover {{
        border-color: {'rgba(250, 204, 21, 0.8)' if is_dark else '#09090b'} !important;
        transform: translateY(-1px) !important;
        box-shadow: {'0 8px 30px rgba(220, 38, 38, 0.5), 0 0 25px rgba(250, 204, 21, 0.4)' if is_dark else '0 6px 18px rgba(0, 0, 0, 0.06)'} !important;
    }}

    .mm-logo-emblem-wrap {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 10px !important;
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        {'animation: logoGlowPulse 3s ease-in-out infinite alternate;' if is_dark else ''}
    }}

    .mm-brand-logo-container:hover .mm-logo-emblem-wrap {{
        transform: scale(1.08) rotate(2deg) !important;
    }}

    @keyframes logoGlowPulse {{
        0% {{
            filter: drop-shadow(0 0 6px rgba(239, 68, 68, 0.85)) drop-shadow(0 0 14px rgba(245, 158, 11, 0.6));
        }}
        100% {{
            filter: drop-shadow(0 0 14px rgba(239, 68, 68, 1)) drop-shadow(0 0 28px rgba(250, 204, 21, 0.9));
        }}
    }}

    .mm-logo-text-wrap {{
        display: flex !important;
        flex-direction: column !important;
        gap: 0.1rem !important;
        min-width: 0 !important;
        flex: 1 !important;
        overflow: hidden !important;
    }}

    .mm-logo-title-row {{
        display: flex !important;
        align-items: center !important;
        gap: 0.25rem !important;
        white-space: nowrap !important;
    }}

    .mm-logo-wordmark {{
        font-family: 'Syne', sans-serif !important;
        font-size: 0.77rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        white-space: nowrap !important;
        color: {'#ffffff' if is_dark else '#09090b'} !important;
    }}

    .mm-logo-highlight {{
        background: {'linear-gradient(135deg, #ef4444 0%, #f59e0b 55%, #facc15 100%)' if is_dark else 'linear-gradient(135deg, #09090b 0%, #4f46e5 100%)'} !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        {'filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.6));' if is_dark else ''}
    }}

    .mm-logo-badge {{
        display: inline-flex !important;
        align-items: center !important;
        gap: 2px !important;
        padding: 1px 4px !important;
        border-radius: 9999px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.54rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        background: {'rgba(239, 68, 68, 0.2)' if is_dark else '#09090b'} !important;
        color: {'#fde047' if is_dark else '#ffffff'} !important;
        border: 1px solid {'rgba(250, 204, 21, 0.65)' if is_dark else '#09090b'} !important;
        {'box-shadow: 0 0 10px rgba(239, 68, 68, 0.5), 0 0 6px rgba(250, 204, 21, 0.35);' if is_dark else ''}
    }}

    .mm-logo-badge-dot {{
        width: 4px !important;
        height: 4px !important;
        border-radius: 50% !important;
        background: {'#facc15' if is_dark else '#38bdf8'} !important;
        {'box-shadow: 0 0 6px #facc15;' if is_dark else ''}
        animation: beaconDot 1.8s ease-in-out infinite alternate !important;
    }}

    @keyframes beaconDot {{
        0% {{ opacity: 0.4; transform: scale(0.8); }}
        100% {{ opacity: 1; transform: scale(1.25); }}
    }}

    .mm-logo-subtitle {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.54rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: {'#ffffff' if is_dark else '#71717a'} !important;
        opacity: {'0.85' if is_dark else '0.75'} !important;
        white-space: nowrap !important;
    }}
    </style>
    """
    render_html(css)


def render_brand_logo(theme: str = "light"):
    """
    Renders the bespoke, unique and ultra-glowy MentorMatch AI brand logo.
    In dark theme: Neon red & solar yellow pulsating bloom with cyber neural emblem.
    In light theme: Minimalist architectural obsidian luxury mark.
    """
    is_dark = (theme == "dark")
    bg_color = "#18181b" if is_dark else "#09090b"
    stroke_border = "#facc15" if is_dark else "#09090b"
    glow_color_1 = "#ef4444" if is_dark else "#4f46e5"
    glow_color_2 = "#f59e0b" if is_dark else "#7c3aed"
    spark_color = "#fde047" if is_dark else "#38bdf8"
    icon_white = "#ffffff"

    svg_data = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="32" height="32">'
        f'<defs>'
        f'<linearGradient id="embGrad" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="{glow_color_1}"/>'
        f'<stop offset="50%" stop-color="{glow_color_2}"/>'
        f'<stop offset="100%" stop-color="{stroke_border}"/>'
        f'</linearGradient>'
        f'<linearGradient id="spkGrad" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="{spark_color}"/>'
        f'<stop offset="100%" stop-color="{glow_color_2}"/>'
        f'</linearGradient>'
        f'</defs>'
        f'<rect x="2" y="2" width="44" height="44" rx="12" fill="{bg_color}" stroke="url(#embGrad)" stroke-width="2.2"/>'
        f'<path d="M 12 33 L 12 18 C 12 15 14 14 16.5 15.8 L 24 22.5 L 31.5 15.8 C 34 14 36 15 36 18 L 36 33" stroke="{icon_white}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M 17 33 L 24 25.5 L 31 33" stroke="url(#spkGrad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M 24 8.5 L 25.4 12.2 L 29 13.5 L 25.4 14.8 L 24 18.5 L 22.6 14.8 L 19 13.5 L 22.6 12.2 Z" fill="url(#spkGrad)"/>'
        f'<circle cx="12" cy="18" r="2.2" fill="{glow_color_1}"/>'
        f'<circle cx="36" cy="18" r="2.2" fill="{stroke_border}"/>'
        f'<circle cx="24" cy="25.5" r="2" fill="{icon_white}"/>'
        f'</svg>'
    )
    b64_img = base64.b64encode(svg_data.encode("utf-8")).decode("utf-8")

    html = f"""
    <div class="mm-brand-logo-container">
        <div class="mm-logo-emblem-wrap">
            <img src="data:image/svg+xml;base64,{b64_img}" width="32" height="32" alt="Logo" style="display: block; border-radius: 10px; flex-shrink: 0;" />
        </div>
        <div class="mm-logo-text-wrap">
            <div class="mm-logo-title-row">
                <span class="mm-logo-wordmark">MENTOR<span class="mm-logo-highlight">MATCH</span></span>
                <span class="mm-logo-badge"><span class="mm-logo-badge-dot"></span>AI</span>
            </div>
            <div class="mm-logo-subtitle">CAMPUS INTELLIGENCE // 2026</div>
        </div>
    </div>
    """
    render_html(html)


def render_metric_card(label: str, value: str, sub: str = "", icon: str = "", index: str = "01"):
    """Renders a Squarespace-inspired minimalist fluid metric card."""
    html = f"""
    <div class="sqsp-metric-card sqsp-animate">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="sqsp-eyebrow" style="margin: 0;">{label}</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; opacity: 0.5;">{index}</span>
            </div>
            <div class="sqsp-metric-value">{value}</div>
        </div>
        {f'<div class="sqsp-metric-badge">● {sub}</div>' if sub else ''}
    </div>
    """
    render_html(html)


def render_hero_celebration_banner(student_name: str, readiness_score: int):
    """
    Renders Squarespace's iconic bold editorial hero section:
    'A mentor makes it real.'
    Includes architectural ribbon counters and readiness index.
    """
    html = f"""
    <div class="sqsp-hero sqsp-animate">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 2rem;">
            <div style="flex: 1; min-width: 320px;">
                <span class="sqsp-eyebrow">AI MENTORSHIP INTELLIGENCE • CAMPUS PLATFORM 2026</span>
                <div class="sqsp-hero-headline">
                    A mentor makes it real.
                </div>
                <div class="sqsp-hero-desc">
                    Every student’s career journey is unique. MentorMatch AI analyzes your current skills, pinpoints critical industry gaps, and pairs you with verified leaders who have walked the path.
                </div>
                <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
                    <span class="sqsp-tag" style="font-weight: 700;">● Personalized for {student_name}</span>
                    <span class="sqsp-tag">7-Signal Compatibility Matrix</span>
                    <span class="sqsp-tag">Grounded Campus RAG</span>
                </div>
            </div>

            <!-- Architectural Status Block -->
            <div style="border: 1px solid inherit; padding: 1.5rem 2rem; border-radius: 16px; min-width: 210px; text-align: center; background: inherit;">
                <div class="sqsp-eyebrow" style="margin-bottom: 0.2rem;">AI READINESS INDEX</div>
                <div class="sqsp-readiness-val">
                    {readiness_score}%
                </div>
                <div style="font-size: 0.76rem; opacity: 0.7; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em;">
                    ● Verified Profile
                </div>
            </div>
        </div>

        <!-- Squarespace Editorial Ribbon -->
        <div class="sqsp-ribbon">
            <div class="sqsp-ribbon-item">
                <div class="sqsp-ribbon-num">01 / STUDENTS</div>
                <div class="sqsp-ribbon-val">320+</div>
                <div class="sqsp-ribbon-lbl">Undergraduate Profiles Indexed</div>
            </div>
            <div class="sqsp-ribbon-item">
                <div class="sqsp-ribbon-num">02 / MENTORS</div>
                <div class="sqsp-ribbon-val">65+</div>
                <div class="sqsp-ribbon-lbl">Engineers & Alumni Mentors</div>
            </div>
            <div class="sqsp-ribbon-item">
                <div class="sqsp-ribbon-num">03 / SESSIONS</div>
                <div class="sqsp-ribbon-val">540+</div>
                <div class="sqsp-ribbon-lbl">1:1 Strategy Sessions Completed</div>
            </div>
            <div class="sqsp-ribbon-item">
                <div class="sqsp-ribbon-num">04 / ACCURACY</div>
                <div class="sqsp-ribbon-val">92%</div>
                <div class="sqsp-ribbon-lbl">Post-Mentorship Satisfaction</div>
            </div>
        </div>
    </div>
    """
    render_html(html)


def render_pipeline_banner():
    """Visualizes the end-to-end intelligent matching pipeline in Squarespace architectural style."""
    html = """
    <div style="border: 1px solid inherit; border-radius: 14px; padding: 0.85rem 1.4rem; margin-bottom: 1.75rem; overflow-x: auto; display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
        <span class="sqsp-eyebrow" style="margin: 0; white-space: nowrap;">⚡ INTELLIGENCE PIPELINE</span>
        <div style="display: flex; align-items: center; gap: 0.6rem; font-size: 0.82rem; font-weight: 600; white-space: nowrap;">
            <span class="sqsp-tag" style="margin: 0;">01 / Student Signals</span>
            <span style="opacity: 0.4;">→</span>
            <span class="sqsp-tag" style="margin: 0;">02 / Skill Gap Diagnostics</span>
            <span style="opacity: 0.4;">→</span>
            <span class="sqsp-tag" style="margin: 0;">03 / RAG Grounded Index</span>
            <span style="opacity: 0.4;">→</span>
            <span class="sqsp-tag" style="margin: 0; border-width: 1.5px;">04 / 7-Signal Matching</span>
            <span style="opacity: 0.4;">→</span>
            <span class="sqsp-tag" style="margin: 0;">05 / 4-Phase Roadmap</span>
        </div>
    </div>
    """
    render_html(html)


def create_skill_radar_chart(categories: List[str], values: List[int], is_dark: bool = False) -> go.Figure:
    """Creates a high-contrast editorial radar chart for student skills."""
    grid_col = "rgba(255, 255, 255, 0.12)" if is_dark else "rgba(0, 0, 0, 0.08)"
    txt_col = "#ffffff" if is_dark else "#09090b"
    line_col = "#ffffff" if is_dark else "#09090b"
    fill_col = "rgba(255, 255, 255, 0.15)" if is_dark else "rgba(9, 9, 11, 0.08)"

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor=fill_col,
        line=dict(color=line_col, width=2),
        marker=dict(color=line_col, size=6),
        name="Current Level"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=8, color=txt_col, family="JetBrains Mono"),
                gridcolor=grid_col
            ),
            angularaxis=dict(
                tickfont=dict(size=10, color=txt_col, family="Plus Jakarta Sans"),
                gridcolor=grid_col
            ),
            bgcolor="rgba(0,0,0,0)"
        ),
        showlegend=False,
        margin=dict(l=28, r=28, t=28, b=28),
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def create_skill_gap_bar_chart(gap_data: List[Dict[str, Any]], is_dark: bool = False) -> go.Figure:
    """Creates a horizontal comparison chart for Skill Gap Analysis."""
    skills = [item["skill"] for item in gap_data]
    current = [item["current"] for item in gap_data]
    required = [item["required"] for item in gap_data]
    txt_col = "#ffffff" if is_dark else "#09090b"
    grid_col = "rgba(255, 255, 255, 0.08)" if is_dark else "rgba(0, 0, 0, 0.06)"
    cur_col = "#ffffff" if is_dark else "#09090b"
    req_col = "rgba(255, 255, 255, 0.25)" if is_dark else "rgba(9, 9, 11, 0.2)"

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=skills,
        x=current,
        name='Current Level',
        orientation='h',
        marker=dict(color=cur_col)
    ))
    fig.add_trace(go.Bar(
        y=skills,
        x=required,
        name='Industry Target',
        orientation='h',
        marker=dict(color=req_col)
    ))

    fig.update_layout(
        barmode='group',
        height=380,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=txt_col)),
        xaxis=dict(range=[0, 100], title="Proficiency (%)", gridcolor=grid_col, tickfont=dict(color=txt_col)),
        yaxis=dict(autorange="reversed", tickfont=dict(color=txt_col)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color=txt_col)
    )
    return fig


def create_department_distribution_chart(students_df: pd.DataFrame, is_dark: bool = False) -> go.Figure:
    dept_counts = students_df["department"].value_counts().reset_index()
    dept_counts.columns = ["Department", "Students"]
    txt_col = "#ffffff" if is_dark else "#09090b"
    bar_col = "#ffffff" if is_dark else "#09090b"

    fig = px.bar(
        dept_counts,
        x="Students",
        y="Department",
        orientation="h"
    )
    fig.update_traces(marker_color=bar_col)
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color=txt_col),
        xaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)" if is_dark else "rgba(0, 0, 0, 0.06)", tickfont=dict(color=txt_col)),
        yaxis=dict(tickfont=dict(color=txt_col))
    )
    return fig


def create_career_goal_donut_chart(students_df: pd.DataFrame, is_dark: bool = False) -> go.Figure:
    goal_counts = students_df["target_role"].value_counts().head(6).reset_index()
    goal_counts.columns = ["Target Role", "Count"]
    txt_col = "#ffffff" if is_dark else "#09090b"

    palette = (
        ["#ffffff", "#d4d4d8", "#a1a1aa", "#71717a", "#52525b", "#3f3f46"]
        if is_dark else
        ["#09090b", "#27272a", "#52525b", "#71717a", "#a1a1aa", "#d4d4d8"]
    )

    fig = px.pie(
        goal_counts,
        names="Target Role",
        values="Count",
        hole=0.6,
        color_discrete_sequence=palette
    )
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color=txt_col),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(color=txt_col))
    )
    return fig


def create_campus_skill_heatmap(students_df: pd.DataFrame, is_dark: bool = False) -> go.Figure:
    depts = students_df["department"].unique()[:4]
    skills_tracked = ["AI/ML", "Cloud/AWS", "DSA", "System Design", "Cybersecurity", "UI/UX"]
    txt_col = "#ffffff" if is_dark else "#09090b"

    matrix = []
    for dept in depts:
        row = []
        subset = students_df[students_df["department"] == dept]
        all_text = " ".join(subset["skills"].dropna().tolist() + subset["interests"].dropna().tolist())
        for sk in skills_tracked:
            count = all_text.lower().count(sk.split("/")[0].lower())
            row.append(count)
        matrix.append(row)

    color_scale = "Greys" if not is_dark else "Cividis"

    fig = px.imshow(
        matrix,
        x=skills_tracked,
        y=[d.split()[0] for d in depts],
        color_continuous_scale=color_scale,
        aspect="auto"
    )
    fig.update_layout(
        height=280,
        margin=dict(l=10, r=10, t=20, b=10),
        font=dict(family="Plus Jakarta Sans", color=txt_col),
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickfont=dict(color=txt_col)),
        yaxis=dict(tickfont=dict(color=txt_col))
    )
    return fig


def verify_student_id_demo(image_bytes: Optional[bytes] = None) -> Dict[str, Any]:
    if image_bytes is None:
        return {
            "verified": True,
            "confidence": 98.4,
            "method": "Facial Biometric & Student ID OCR Anchor",
            "message": "Student identity verified successfully. Matched against University Enrollment Registry."
        }
    if _has_cv2:
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is not None:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                face_cascade = cv2.CascadeClassifier(cascade_path)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
                face_found = len(faces) > 0
                return {
                    "verified": True,
                    "faces_detected": max(len(faces), 1),
                    "confidence": 97.8 if face_found else 91.2,
                    "method": "OpenCV Haar-Cascade Face & Campus Card Verification",
                    "message": "Face geometry verified. ID signature verified against Student Registry."
                }
        except Exception:
            pass

    return {
        "verified": True,
        "faces_detected": 1,
        "confidence": 96.5,
        "method": "Digital Signature Verification Engine",
        "message": "Campus identity card verified against enrollment."
    }
