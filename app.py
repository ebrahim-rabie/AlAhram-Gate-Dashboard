import streamlit as st

# ── Page config must be the FIRST Streamlit command ──────────────────────────
st.set_page_config(page_title="AlAhram Gate Dashboard", page_icon="assets/logo.png", layout="wide", initial_sidebar_state="collapsed")

from utils.theme import inject_custom_css, render_top_header, get_colors
from utils.data_loader import load_all_summary, load_new_vehicles, load_used_vehicles, load_ev_by_license, pd
from utils.charts import (
    kpi_card, section_header, gold_divider,
    donut_chart, horizontal_bar, line_chart, treemap_chart, data_table
)

# Force clear cache to ensure old data isn't shown
st.cache_data.clear()

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
summary = load_all_summary(scope)



# ── Scope-aware KPIs & Data Filtering ──────────────────────────────────────────
if scope == "New Vehicles Only":
    highlight_val = summary.get("total_new", 0)
    highlight_label, highlight_icon = "New Vehicles", "new"
    
    # Extract only new vehicle data for charts
    new_df = load_new_vehicles()
    fuel_dist = new_df.groupby("Fuel_Type", as_index=False)["Grand Total"].sum() if "Fuel_Type" in new_df.columns else pd.DataFrame()
    top_brands = new_df.groupby("Brand", as_index=False)["Grand Total"].sum().sort_values("Grand Total", ascending=False).head(10) if "Brand" in new_df.columns else pd.DataFrame()
    country_dist = new_df.groupby("Country", as_index=False)["Grand Total"].sum() if "Country" in new_df.columns else pd.DataFrame()
    year_trend = pd.DataFrame() # No year data in new vehicles
    
elif scope == "Used Vehicles Only":
    highlight_val = summary.get("total_used", 0)
    highlight_label, highlight_icon = "Used Vehicles", "used"
    
    # Extract only used vehicle data for charts
    used_df = load_used_vehicles()
    fuel_dist = used_df.groupby("Fuel_Type", as_index=False)["Grand Total"].sum() if "Fuel_Type" in used_df.columns else pd.DataFrame()
    top_brands = used_df.groupby("Brand", as_index=False)["Grand Total"].sum().sort_values("Grand Total", ascending=False).head(10) if "Brand" in used_df.columns else pd.DataFrame()
    country_dist = pd.DataFrame() # No country data in used vehicles
    year_trend = summary.get("year_trend", pd.DataFrame()) # Keep global year trend for used

elif scope == "EVs Only":
    highlight_val = summary.get("total_ev", 0)
    highlight_label, highlight_icon = "Electric Vehicles", "electric"
    
    # Extract only EV data for charts
    ev_df = load_ev_by_license()
    fuel_dist = ev_df.groupby("Fuel_Type", as_index=False)["Grand Total"].sum() if "Fuel_Type" in ev_df.columns else pd.DataFrame()
    top_brands = ev_df.groupby("Brand", as_index=False)["Grand Total"].sum().sort_values("Grand Total", ascending=False).head(10) if "Brand" in ev_df.columns else pd.DataFrame()
    country_dist = ev_df.groupby("Country", as_index=False)["Grand Total"].sum() if "Country" in ev_df.columns else pd.DataFrame()
    year_trend = pd.DataFrame() # No year data in EVs

else:
    highlight_val = summary.get("total_all", 0)
    highlight_label, highlight_icon = "Total Private & EV", "car"
    
    # Default global summary
    fuel_dist = summary.get("fuel_dist")
    top_brands = summary.get("top_brands")
    country_dist = summary.get("country_dist")
    year_trend = summary.get("year_trend")

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

if scope == "All Datasets":
    st.markdown("<div style='text-align: center; color: #8b949e; font-size: 0.9rem; margin-top: -10px; margin-bottom: 20px;'>💡 <b>Note:</b> This dashboard focuses exclusively on the <b>Private</b> and <b>Electric Vehicle</b> sectors. For the comprehensive market analysis across all license types (434k+ vehicles), please visit the <i>Market Distribution</i> page.</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# ── Row 1: Fuel Distribution  |  Top Brands ────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    if fuel_dist is not None and not fuel_dist.empty:
        donut_chart(
            df=fuel_dist,
            names="Fuel_Type",
            values="Grand Total",
            title=f"Fuel Type Distribution ({highlight_label})",
        )
    else:
        st.info("No fuel-type distribution data available for this scope.")

with col_right:
    if top_brands is not None and not top_brands.empty:
        horizontal_bar(
            df=top_brands.head(10),
            x="Grand Total",
            y="Brand",
            title=f"Top 10 Brands ({highlight_label})",
            n=10,
        )
    else:
        st.info("No brand data available for this scope.")

# ── Row 2: Country Treemap  |  Year Trend ──────────────────────────────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    if country_dist is not None and not country_dist.empty:
        treemap_chart(
            df=country_dist,
            path=["Country"],
            values="Grand Total",
            title=f"Registrations by Country of Origin ({highlight_label})",
            height=450,
        )
    else:
        st.info("No country distribution data available for this scope.")

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
        st.info("No yearly trend data available for this scope.")

# ── Summary data tables ────────────────────────────────────────────────────
gold_divider()

if top_brands is not None and not top_brands.empty:
    data_table(df=top_brands, title="All Brands Summary")
