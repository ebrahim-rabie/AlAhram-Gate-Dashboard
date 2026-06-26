"""
AlAhram Gate Dashboard — Dual Theme Engine
Provides dark/light mode support with Al-Ahram brand colors.
"""

import streamlit as st
import base64
from pathlib import Path


# ── Color Palettes ──────────────────────────────────────────────────────────

DARK_THEME = {
    "bg_primary": "#0D1117",   # Soft Midnight Slate
    "bg_secondary": "#161B22", # Slightly lighter (Sidebar)
    "bg_card": "#1E232B",      # Soft Surface (Cards)
    "text_primary": "#FFFFFF",
    "text_secondary": "#B0B0B0",
    "accent_red": "#E06C75",  # Soft Crimson (Eye-friendly)
    "accent_gold": "#D4A84B",
    "accent_bright": "#F0B429",
    "border": "#3A3A4A",
    "positive": "#00C853",
    "negative": "#FF4B4B",
    "plotly_bg": "rgba(0,0,0,0)",
    "plotly_paper": "rgba(0,0,0,0)",
    "plotly_grid": "#3A3A4A",
    "plotly_text": "#FFFFFF",
}


CHART_COLORS = [
    # Midnight & Gold
    "#D4A84B",  # Pure Gold
    "#1D3557",  # Deep Navy
    "#E63946",  # Ruby Red
    # Oceanic
    "#45B7D1",  # Sky Blue
    "#2A9D8F",  # Deep Teal
    "#48CAE4",  # Turquoise
    # Cyber Neon
    "#00F5D4",  # Neon Cyan
    "#F15BB5",  # Neon Magenta
    "#9B5DE5",  # Electric Purple
    # Nord / Pastel
    "#E06C75",  # Soft Crimson
    "#98C379",  # Soft Green
    "#E5C07B",  # Soft Yellow
    "#61AFEF",  # Soft Blue
    "#C678DD",  # Soft Lavender
    "#D19A66",  # Soft Orange
]


def get_colors() -> dict:
    """Get the color palette for the theme."""
    return DARK_THEME


def get_chart_colors() -> list:
    """Get the chart color sequence."""
    return CHART_COLORS


# ── Plotly Template ─────────────────────────────────────────────────────────

def get_plotly_layout() -> dict:
    """Get Plotly layout kwargs for the current theme."""
    colors = get_colors()
    return {
        "paper_bgcolor": colors["plotly_paper"],
        "plot_bgcolor": colors["plotly_bg"],
        "font": {"color": colors["plotly_text"], "family": "Inter, sans-serif"},
        "xaxis": {
            "gridcolor": colors["plotly_grid"],
            "zerolinecolor": colors["plotly_grid"],
        },
        "yaxis": {
            "gridcolor": colors["plotly_grid"],
            "zerolinecolor": colors["plotly_grid"],
        },
        "margin": {"l": 20, "r": 20, "t": 50, "b": 20},
        "hoverlabel": {
            "bgcolor": colors["bg_card"],
            "font_color": colors["text_primary"],
            "bordercolor": colors["accent_red"],
        },
        "legend": {
            "bgcolor": "rgba(0,0,0,0)",
            "font": {"color": colors["plotly_text"]},
        },
        "colorway": CHART_COLORS,
    }


# ── Logo Helper ─────────────────────────────────────────────────────────────

def _get_logo_base64() -> str:
    """Load and encode the logo as base64."""
    logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


# ── Custom CSS Injection ────────────────────────────────────────────────────

def inject_custom_css():
    """Inject theme-aware custom CSS into the Streamlit page."""
    colors = get_colors()
    logo_b64 = _get_logo_base64()
    
    # Background watermark
    watermark_css = ""
    if logo_b64:
        watermark_css = f"""
        /* ── Logo Background Watermark ─────────────────── */
        [data-testid="stAppViewContainer"] {{
            /* Blend the logo with an 85% opaque layer of the Midnight background color */
            background-image: linear-gradient(rgba(13, 17, 23, 0.85), rgba(13, 17, 23, 0.85)), url("data:image/png;base64,{logo_b64}") !important;
            background-repeat: no-repeat !important;
            background-position: center center !important;
            background-attachment: fixed !important;
            background-size: 60vh !important;
        }}
        """

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ────────────────────────────────────── */
    .stApp {{
        font-family: 'Inter', sans-serif;
    }}

    {watermark_css}

    /* ── Top accent bar ────────────────────────────── */
    .stApp > header {{
        border-top: 3px solid {colors['accent_red']};
    }}

    /* ── KPI Metric Card ───────────────────────────── */
    .kpi-card {{
        background: {colors['bg_card']};
        border: 1px solid {colors['border']};
        border-left: 4px solid {colors['accent_red']};
        border-radius: 12px;
        padding: 20px 18px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 6px 20px rgba(200, 16, 46, 0.15);
        border-left-color: {colors['accent_gold']};
    }}
    .kpi-icon {{
        font-size: 28px;
        margin-bottom: 6px;
    }}
    .kpi-value {{
        font-size: 28px;
        font-weight: 700;
        color: {colors['accent_red']};
        margin: 4px 0;
        letter-spacing: -0.5px;
    }}
    .kpi-label {{
        font-size: 13px;
        color: {colors['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
    }}
    .kpi-delta {{
        font-size: 12px;
        margin-top: 4px;
        font-weight: 500;
    }}
    .kpi-delta.positive {{
        color: {colors['positive']};
    }}
    .kpi-delta.negative {{
        color: {colors['negative']};
    }}

    /* ── Section Header ────────────────────────────── */
    .section-header {{
        font-size: 20px;
        font-weight: 600;
        color: {colors['text_primary']};
        padding-bottom: 8px;
        border-bottom: 3px solid {colors['accent_gold']};
        margin: 30px 0 20px 0;
        display: inline-block;
    }}

    /* Top Header Styles */
    .top-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 1rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid {colors['accent_gold']};
    }}
    .top-logo-container {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}
    .top-logo-container img {{
        height: 60px;
    }}
    .top-logo-container .top-title {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: {colors['text_primary']};
        letter-spacing: 1px;
    }}

    /* ── Theme Toggle Button ───────────────────────── */
    .theme-toggle {{
        text-align: center;
        margin: 10px 0 20px 0;
    }}

    /* ── Chart Container ───────────────────────────── */
    .chart-container {{
        background: {colors['bg_card']};
        border: 1px solid {colors['border']};
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
    }}

    /* ── Dataframe styling ─────────────────────────── */
    .stDataFrame {{
        border-radius: 10px;
        overflow: hidden;
    }}

    /* ── Divider ───────────────────────────────────── */
    .gold-divider {{
        height: 2px;
        background: linear-gradient(90deg, {colors['accent_red']}, {colors['accent_gold']}, transparent);
        border: none;
        margin: 20px 0;
    }}

    /* ── Hide Streamlit branding ───────────────────── */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* ── Radio buttons style ───────────────────────── */
    .stRadio > div {{
        gap: 0.3rem;
    }}

    /* ── Tabs styling ──────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ── Top Header Renderer ───────────────────────────────────────────────────────

def render_top_header():
    """Render the top header with logo."""
    logo_b64 = _get_logo_base64()

    if logo_b64:
        st.markdown(
            f"""
            <div class="top-header">
                <div class="top-logo-container">
                    <img src="data:image/png;base64,{logo_b64}" alt="Al-Ahram Logo">
                    <div class="top-title">Gate Dashboard</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown("## 🏛️ AlAhram Gate Dashboard")
