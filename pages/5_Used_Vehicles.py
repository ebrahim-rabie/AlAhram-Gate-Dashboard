import streamlit as st

# ── Page config (must be first Streamlit command) ──────────────────────────
st.set_page_config(page_title="Used Vehicles | AlAhram", page_icon="assets/logo.png", layout="wide", initial_sidebar_state="collapsed")

import pandas as pd
from utils.theme import inject_custom_css, render_top_header, get_colors
from utils.charts import (
    kpi_card, section_header, gold_divider,
    donut_chart, horizontal_bar, line_chart,
    treemap_chart, egypt_map_chart, data_table,
)
from utils.data_loader import load_used_vehicles
inject_custom_css()
render_top_header()

# ── Load data ──────────────────────────────────────────────────────────────
df = load_used_vehicles()
colors = get_colors()

# ── Year columns ───────────────────────────────────────────────────────────
YEAR_COLS = [2022, 2023, 2024, 2025, 2026]

# ── Top Filters ───────────────────────────────────────────────────────
with st.expander(":material/search: Search & Filters", expanded=False):
    fcol1, fcol2, fcol3, fcol4 = st.columns(4)
    
    with fcol1:
        provinces = sorted(df["Province"].dropna().unique())
        sel_provinces = st.multiselect("Province", provinces, default=[])
        
    with fcol2:
        # Traffic Unit (cascading based on Province)
        temp_df = df[df['Province'].isin(sel_provinces)] if sel_provinces else df
        tu_opts = sorted(temp_df["Traffic Unit"].dropna().unique().tolist()) if "Traffic Unit" in temp_df.columns else []
        sel_traffic = st.multiselect("Traffic Unit", tu_opts, help="Auto-filtered by selected Province")
        
    with fcol3:
        brands = sorted(df["Brand"].dropna().unique())
        sel_brands = st.multiselect("Brand", brands, default=[])
        
    with fcol4:
        country_opts = sorted(df["Country"].dropna().unique().tolist()) if "Country" in df.columns else []
        sel_country = st.multiselect("Country", country_opts)
        
    fcol5, fcol6, fcol7 = st.columns([1, 1, 2])
    
    with fcol5:
        fuel_types = sorted(df["Fuel_Type"].dropna().unique())
        sel_fuel = st.multiselect("Fuel Type", fuel_types, default=[])
        
    with fcol6:
        shapes = sorted(df["Shape"].dropna().unique())
        sel_shapes = st.multiselect("Shape", shapes, default=[])
        
    with fcol7:
        st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
        year_range = st.slider(
            "Year Range", 
            min_value=min(YEAR_COLS), 
            max_value=max(YEAR_COLS), 
            value=(min(YEAR_COLS), max(YEAR_COLS)),
            step=1,
            help="Filter registrations by specific years"
        )

# ── Apply filters ──────────────────────────────────────────────────────────
filtered = df.copy()

if sel_provinces:
    filtered = filtered[filtered["Province"].isin(sel_provinces)]
if sel_traffic:
    filtered = filtered[filtered["Traffic Unit"].isin(sel_traffic)]
if sel_brands:
    filtered = filtered[filtered["Brand"].isin(sel_brands)]
if sel_fuel:
    filtered = filtered[filtered["Fuel_Type"].isin(sel_fuel)]
if sel_shapes:
    filtered = filtered[filtered["Shape"].isin(sel_shapes)]
if sel_country:
    filtered = filtered[filtered["Country"].isin(sel_country)]

# Update YEAR_COLS based on slider
active_years = [yr for yr in YEAR_COLS if year_range[0] <= yr <= year_range[1]]

# Recompute Grand Total based on active years only
if active_years:
    filtered["Grand Total"] = filtered[active_years].sum(axis=1)
else:
    filtered["Grand Total"] = 0

# ── Page title ─────────────────────────────────────────────────────────────
st.markdown("## :material/sync: Used Vehicles Market")
gold_divider()

# ── Guard against empty data ──────────────────────────────────────────────
if filtered.empty:
    st.warning("No data matches the selected filters. Please adjust your selections.")
    st.stop()

# ── KPI calculations ──────────────────────────────────────────────────────
total_used = int(filtered["Grand Total"].sum())

top_brand = (
    filtered.groupby("Brand")["Grand Total"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

# Peak year: year column with highest aggregate sum
year_sums = {yr: int(filtered[yr].sum()) for yr in YEAR_COLS if yr in filtered.columns}
peak_year = max(year_sums, key=year_sums.get) if year_sums else "N/A"

top_province = (
    filtered.groupby("Province")["Grand Total"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

# ── KPI cards ──────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total Used Vehicles", f"{total_used:,}", "used")
with k2:
    kpi_card("Top Brand", top_brand, "trophy")
with k3:
    kpi_card("Peak Year", str(peak_year), "calendar")
with k4:
    kpi_card("Top Province", top_province, "location")

st.markdown("")

# ── 1. Year-over-Year Trend (full width, area chart) ─────────────────────
section_header(":material/show_chart: Year-over-Year Registration Trend")
year_trend_df = pd.DataFrame(
    {"Year": [str(yr) for yr in YEAR_COLS], "Registrations": [year_sums.get(yr, 0) for yr in YEAR_COLS]}
)
line_chart(year_trend_df, x="Year", y="Registrations", title="Used Vehicle Registrations by Year", height=420, area=True)

# ── 2. Top Brands & Top Provinces (two columns) ──────────────────────────
section_header(":material/insights: Brand & Province Analysis")
col1, col2 = st.columns(2)

with col1:
    brand_df = (
        filtered.groupby("Brand", as_index=False)["Grand Total"]
        .sum()
        .sort_values("Grand Total", ascending=False)
    )
    horizontal_bar(brand_df, x="Grand Total", y="Brand", title="Top 15 Used Brands", n=15)

with col2:
    prov_df = (
        filtered.groupby("Province", as_index=False)["Grand Total"]
        .sum()
        .sort_values("Grand Total", ascending=False)
    )
    egypt_map_chart(prov_df, prov_col="Province", val_col="Grand Total", title="Provincial Distribution Map", height=450)

# ── 3. Fuel Type & Country of Origin (two columns) ───────────────────────
section_header(":material/public: Fuel Type & Country of Origin")
col3, col4 = st.columns(2)

with col3:
    fuel_df = (
        filtered.groupby("Fuel_Type", as_index=False)["Grand Total"]
        .sum()
        .sort_values("Grand Total", ascending=False)
    )
    donut_chart(fuel_df, names="Fuel_Type", values="Grand Total", title="Fuel Type Distribution")

with col4:
    country_df = (
        filtered.groupby("Country", as_index=False)["Grand Total"]
        .sum()
        .sort_values("Grand Total", ascending=False)
    )
    treemap_chart(country_df, path=["Country"], values="Grand Total", title="Country of Origin")

# ── 4. Vehicle Shape Distribution (full width donut) ─────────────────────
section_header(":material/bar_chart: Vehicle Shape Distribution")
shape_df = (
    filtered.groupby("Shape", as_index=False)["Grand Total"]
    .sum()
    .sort_values("Grand Total", ascending=False)
)
horizontal_bar(shape_df, x="Grand Total", y="Shape", title="Used Vehicles by Shape", n=15)

# ── 5. Data table ─────────────────────────────────────────────────────────
section_header(":material/dataset: Detailed Data")
data_table(filtered, title="Used Vehicles Data")
