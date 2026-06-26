"""
AlAhram Gate Dashboard — Reusable Chart Components
Theme-aware Plotly chart builders and KPI cards.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.theme import get_colors, get_plotly_layout, get_chart_colors


# ── KPI Card ────────────────────────────────────────────────────────────────

def kpi_card(title: str, value, icon: str = "📊", delta: str = None, delta_positive: bool = True):
    """Render a styled KPI metric card."""
    from utils.icons import get_svg_icon
    
    colors = get_colors()
    formatted_value = f"{value:,}" if isinstance(value, (int, float)) else str(value)

    delta_html = ""
    if delta:
        delta_class = "positive" if delta_positive else "negative"
        delta_icon = "▲" if delta_positive else "▼"
        delta_html = f'<div class="kpi-delta {delta_class}">{delta_icon} {delta}</div>'

    # If the icon string doesn't look like an emoji/text (i.e. it's a known key or SVG), get it.
    # Otherwise, fallback gracefully.
    svg_html = get_svg_icon(icon) if len(icon) > 2 else icon

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon" style="color: {colors['accent_red']};">{svg_html}</div>
            <div class="kpi-label">{title}</div>
            <div class="kpi-value">{formatted_value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Section Header ──────────────────────────────────────────────────────────

def section_header(title: str):
    """Render a styled section header with gold underline."""
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def gold_divider():
    """Render a gradient divider."""
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)


# ── Donut Chart ─────────────────────────────────────────────────────────────

def donut_chart(df: pd.DataFrame, names: str, values: str, title: str = "", height: int = 400):
    """Create a themed donut chart."""
    layout = get_plotly_layout()
    colors = get_chart_colors()

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.55,
        color_discrete_sequence=colors,
    )
    fig.update_traces(
        textposition="outside",
        textinfo="label+percent",
        textfont_size=11,
        marker=dict(line=dict(color=layout.get("font", {}).get("color", "#FFF"), width=1)),
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=height,
        showlegend=False,
        **{k: v for k, v in layout.items() if k not in ["xaxis", "yaxis"]},
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Horizontal Bar Chart ───────────────────────────────────────────────────

def horizontal_bar(df: pd.DataFrame, x: str, y: str, title: str = "", n: int = 15, height: int = 450, color: str = None):
    """Create a themed horizontal bar chart (top N)."""
    layout = get_plotly_layout()
    colors = get_colors()

    # Sort and take top N
    plot_df = df.nlargest(n, x).sort_values(x, ascending=True)

    bar_color = color or colors["accent_red"]

    fig = go.Figure(
        go.Bar(
            x=plot_df[x],
            y=plot_df[y],
            orientation="h",
            marker=dict(
                color=bar_color,
                line=dict(color=colors["accent_gold"], width=0.5),
            ),
            text=plot_df[x].apply(lambda v: f"{v:,.0f}"),
            textposition="outside",
            textfont=dict(size=11),
        )
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=height,
        **layout,
    )
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")
    st.plotly_chart(fig, use_container_width=True)


# ── Stacked Bar Chart ──────────────────────────────────────────────────────

def stacked_bar(df: pd.DataFrame, x: str, y: str, color: str, title: str = "", height: int = 450):
    """Create a themed stacked bar chart."""
    layout = get_plotly_layout()
    chart_colors = get_chart_colors()

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        color_discrete_sequence=chart_colors,
        barmode="stack",
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=height,
        **layout,
    )
    fig.update_xaxes(title_text="", tickangle=-45)
    fig.update_yaxes(title_text="")
    st.plotly_chart(fig, use_container_width=True)


# ── Line / Area Chart ──────────────────────────────────────────────────────

def line_chart(df: pd.DataFrame, x: str, y: str, title: str = "", height: int = 400, area: bool = False):
    """Create a themed line or area chart."""
    layout = get_plotly_layout()
    colors = get_colors()

    fig = go.Figure()

    if area:
        fig.add_trace(
            go.Scatter(
                x=df[x],
                y=df[y],
                mode="lines+markers",
                fill="tozeroy",
                fillcolor=f"rgba(200, 16, 46, 0.15)",
                line=dict(color=colors["accent_red"], width=3),
                marker=dict(size=10, color=colors["accent_gold"], line=dict(color=colors["accent_red"], width=2)),
                text=df[y].apply(lambda v: f"{v:,.0f}"),
                textposition="top center",
            )
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=df[x],
                y=df[y],
                mode="lines+markers+text",
                line=dict(color=colors["accent_red"], width=3),
                marker=dict(size=10, color=colors["accent_gold"], line=dict(color=colors["accent_red"], width=2)),
                text=df[y].apply(lambda v: f"{v:,.0f}"),
                textposition="top center",
                textfont=dict(size=11),
            )
        )

    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=height,
        showlegend=False,
        **layout,
    )
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")
    st.plotly_chart(fig, use_container_width=True)


# ── Treemap Chart ───────────────────────────────────────────────────────────

def treemap_chart(df: pd.DataFrame, path: list, values: str, title: str = "", height: int = 450):
    """Create a themed treemap chart."""
    layout = get_plotly_layout()
    chart_colors = get_chart_colors()

    fig = px.treemap(
        df,
        path=path,
        values=values,
        color_discrete_sequence=chart_colors,
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=height,
        **{k: v for k, v in layout.items() if k not in ["xaxis", "yaxis"]},
    )
    fig.update_traces(
        textinfo="label+value+percent parent",
        textfont_size=12,
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Heatmap Chart ───────────────────────────────────────────────────────────

def heatmap_chart(df: pd.DataFrame, x: str, y: str, z: str, title: str = "", height: int = 500):
    """Create a themed heatmap chart."""
    layout = get_plotly_layout()
    colors = get_colors()

    pivot = df.pivot_table(index=y, columns=x, values=z, aggfunc="sum", fill_value=0)

    fig = go.Figure(
        go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale=[
                [0, colors["bg_card"]],
                [0.5, colors["accent_gold"]],
                [1, colors["accent_red"]],
            ],
            text=pivot.values,
            texttemplate="%{text:,.0f}",
            textfont={"size": 10},
            hovertemplate="%{y} × %{x}: %{z:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=height,
        **layout,
    )
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)


# ── Histogram Chart ─────────────────────────────────────────────────────────

def histogram_chart(df: pd.DataFrame, x: str, title: str = "", height: int = 400, nbins: int = 30):
    """Create a themed histogram."""
    layout = get_plotly_layout()
    colors = get_colors()

    fig = go.Figure(
        go.Histogram(
            x=df[x],
            nbinsx=nbins,
            marker=dict(
                color=colors["accent_red"],
                line=dict(color=colors["accent_gold"], width=1),
            ),
        )
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=height,
        **layout,
    )
    fig.update_xaxes(title_text=x)
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, use_container_width=True)


# ── Box Plot ────────────────────────────────────────────────────────────────

def box_plot(df: pd.DataFrame, x: str, y: str, title: str = "", height: int = 450):
    """Create a themed box plot."""
    layout = get_plotly_layout()
    chart_colors = get_chart_colors()

    fig = px.box(
        df,
        x=x,
        y=y,
        color=x,
        color_discrete_sequence=chart_colors,
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=height,
        showlegend=False,
        **layout,
    )
    fig.update_xaxes(tickangle=-45, title_text="")
    fig.update_yaxes(title_text=y)
    st.plotly_chart(fig, use_container_width=True)


# ── Grouped Bar Chart ──────────────────────────────────────────────────────

def grouped_bar(df: pd.DataFrame, x: str, y: str, color: str, title: str = "", height: int = 450):
    """Create a themed grouped bar chart."""
    layout = get_plotly_layout()
    chart_colors = get_chart_colors()

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        barmode="group",
        color_discrete_sequence=chart_colors,
    )
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=height,
        **layout,
    )
    fig.update_xaxes(tickangle=-45, title_text="")
    fig.update_yaxes(title_text="")
    st.plotly_chart(fig, use_container_width=True)

# ── Egypt Map Chart ─────────────────────────────────────────────────────────

def egypt_map_chart(df: pd.DataFrame, prov_col: str, val_col: str, title: str = "", height: int = 500):
    """Create a bubble map over Egypt for provinces."""
    layout = get_plotly_layout()
    colors = get_colors()
    
    # Predefined coordinates for Egypt Governorates
    prov_coords = {
        "Cairo": (30.0444, 31.2357),
        "Giza": (30.0131, 31.2089),
        "Alexandria": (31.2001, 29.9187),
        "Dakahlia": (31.0364, 31.3807),
        "Red Sea": (26.2540, 34.1118),
        "Beheira": (30.8481, 30.3436),
        "Fayoum": (29.3084, 30.8428),
        "Gharbia": (30.8754, 31.0335),
        "Ismailia": (30.5965, 32.2715),
        "Menoufia": (30.5972, 29.9892),
        "Minya": (28.1099, 30.7503),
        "Qalyubia": (30.4138, 31.1859),
        "New Valley": (24.5456, 27.1735),
        "Suez": (29.9668, 32.5498),
        "Aswan": (24.0889, 32.8998),
        "Assiut": (27.1810, 31.1837),
        "Beni Suef": (29.0661, 31.0994),
        "Port Said": (31.2653, 32.3019),
        "Damietta": (31.4165, 31.8133),
        "Sharkia": (30.5877, 31.5020),
        "South Sinai": (28.9710, 33.6111),
        "Kafr El Sheikh": (31.1107, 30.9388),
        "Matrouh": (31.3525, 27.2373),
        "Luxor": (25.6872, 32.6396),
        "Qena": (26.1642, 32.7267),
        "North Sinai": (30.6085, 33.8033),
        "Sohag": (26.5591, 31.6957)
    }
    
    # Map coordinates to dataframe
    df = df.copy()
    # Ensure English names match the dictionary
    df["lat"] = df[prov_col].map(lambda x: prov_coords.get(x, (None, None))[0])
    df["lon"] = df[prov_col].map(lambda x: prov_coords.get(x, (None, None))[1])
    
    # Drop rows without coordinates
    plot_df = df.dropna(subset=["lat", "lon"])
    
    fig = px.scatter_mapbox(
        plot_df, 
        lat="lat", 
        lon="lon", 
        size=val_col,
        color=val_col,
        hover_name=prov_col, 
        hover_data={val_col: ":,.0f", "lat": False, "lon": False},
        color_continuous_scale=[
            [0, colors["accent_gold"]],
            [1, colors["accent_red"]]
        ],
        size_max=40,
        zoom=4.5,
        center={"lat": 26.8206, "lon": 30.8025},
        mapbox_style="carto-darkmatter"
    )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        height=height,
        margin={"r":0,"t":40,"l":0,"b":0},
        paper_bgcolor=colors["bg_card"],
        font=dict(color=colors["text_primary"]),
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ── Data Table ──────────────────────────────────────────────────────────────

def data_table(df: pd.DataFrame, title: str = "📋 Data Explorer", height: int = 400):
    """Render a searchable, downloadable data table."""
    colors = get_colors()
    section_header(title)

    # Search filter
    search = st.text_input("🔍 Search", key=f"search_{title}", placeholder="Type to filter...")
    if search:
        mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False, na=False).any(), axis=1)
        df = df[mask]

    st.dataframe(
        df,
        height=height,
        use_container_width=True,
        hide_index=True,
    )

    # Download button
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{title.replace(' ', '_').lower()}.csv",
        mime="text/csv",
    )
