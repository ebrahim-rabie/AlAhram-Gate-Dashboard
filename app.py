import streamlit as st

# ── Page config must be the FIRST Streamlit command ──────────────────────────
st.set_page_config(page_title="AlAhram Gate Dashboard", page_icon="assets/logo.png", layout="wide", initial_sidebar_state="collapsed")

from utils.theme import inject_custom_css, render_top_header, get_colors
from utils.data_loader import load_all_summary
from utils.charts import (
    kpi_card, section_header, gold_divider,
    donut_chart, horizontal_bar, line_chart, treemap_chart, data_table
)

# ── Theme & Top Header ─────────────────────────────────────────────────────────
inject_custom_css()
render_top_header()
colors = get_colors()

# ── Top Filter ───────────────────────────────────────────────────────────
with st.expander(":material/tune: Dashboard Settings", expanded=False):
    st.markdown("### 📊 Dataset Scope")
    scope = st.radio(
        "Select the scope of data for the Key Performance Indicators (KPIs):",
        ["All Datasets", "New Vehicles Only", "Used Vehicles Only", "EVs Only"],
        key="home_scope",
        horizontal=True
    )

# ── Load aggregate data ─────────────────────────────────────────────────────
summary = load_all_summary()



# ── Scope-aware KPIs ─────────────────────────────────────────────────────────
if scope == "New Vehicles Only":
    highlight_val = summary.get("total_new", 0)
    highlight_label, highlight_icon = "New Vehicles", "new"
elif scope == "Used Vehicles Only":
    highlight_val = summary.get("total_used", 0)
    highlight_label, highlight_icon = "Used Vehicles", "used"
elif scope == "EVs Only":
    highlight_val = summary.get("total_ev", 0)
    highlight_label, highlight_icon = "Electric Vehicles", "electric"
else:
    highlight_val = summary.get("total_all", 0)
    highlight_label, highlight_icon = "Total Vehicles", "car"

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    kpi_card(title=highlight_label, value=f"{highlight_val:,}", icon=highlight_icon)
with k2:
    kpi_card(title="New Vehicles", value=f"{summary.get('total_new', 0):,}", icon="new")
with k3:
    kpi_card(title="Used Vehicles", value=f"{summary.get('total_used', 0):,}", icon="used")
with k4:
    kpi_card(title="Electric Vehicles", value=f"{summary.get('total_ev', 0):,}", icon="electric")
with k5:
    kpi_card(title="Brands", value=f"{summary.get('total_brands', 0):,}", icon="brand")

# ── Row 1: Fuel Distribution  |  Top Brands ────────────────────────────────
col_left, col_right = st.columns(2)

fuel_dist = summary.get("fuel_dist")
top_brands = summary.get("top_brands")

with col_left:
    if fuel_dist is not None and not fuel_dist.empty:
        donut_chart(
            df=fuel_dist,
            names="Fuel_Type",
            values="Grand Total",
            title="Fuel Type Distribution",
        )
    else:
        st.info("No fuel-type distribution data available.")

with col_right:
    if top_brands is not None and not top_brands.empty:
        horizontal_bar(
            df=top_brands.head(10),
            x="Grand Total",
            y="Brand",
            title="Top 10 Brands",
            n=10,
        )
    else:
        st.info("No brand data available.")

# ── Row 2: Country Treemap  |  Year Trend ──────────────────────────────────
col_left2, col_right2 = st.columns(2)

country_dist = summary.get("country_dist")
year_trend = summary.get("year_trend")

with col_left2:
    if country_dist is not None and not country_dist.empty:
        treemap_chart(
            df=country_dist,
            path=["Country"],
            values="Grand Total",
            title="Vehicles by Country of Origin",
        )
    else:
        st.info("No country distribution data available.")

with col_right2:
    if year_trend is not None and not year_trend.empty:
        line_chart(
            df=year_trend,
            x="Year",
            y="Registrations",
            title="Registration Trend by Year",
            area=True,
        )
    else:
        st.info("No yearly trend data available.")

# ── Summary data tables ────────────────────────────────────────────────────
gold_divider()

if top_brands is not None and not top_brands.empty:
    data_table(df=top_brands, title="All Brands Summary")
