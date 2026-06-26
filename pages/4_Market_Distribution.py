import streamlit as st
import pandas as pd

# --- Page Config (MUST be first Streamlit command) ---
st.set_page_config(page_title="Market | AlAhram", page_icon="assets/logo.png", layout="wide", initial_sidebar_state="collapsed")

from utils.theme import inject_custom_css, render_top_header, get_colors
from utils.charts import (
    kpi_card, section_header, gold_divider,
    donut_chart, horizontal_bar, stacked_bar, treemap_chart, data_table,
)
from utils.data_loader import load_license_condition_gov, load_vehicle_condition

# --- Theme & Sidebar Header ---
inject_custom_css()
render_top_header()
colors = get_colors()

# ──────────────────────────────────────────────
# Top Filters
# ──────────────────────────────────────────────
with st.expander(":material/search: Search & Filters", expanded=False):
    data_view = st.radio("Data View", ["By License Type", "By Vehicle Condition"], horizontal=True)

    # Load the appropriate dataset based on the selected view
    @st.cache_data
    def get_license_data():
        return load_license_condition_gov()

    @st.cache_data
    def get_condition_data():
        return load_vehicle_condition()

    if data_view == "By License Type":
        df_raw = get_license_data()
    else:
        df_raw = get_condition_data()

    fcol1, fcol2, fcol3, fcol4 = st.columns(4)

    # --- Shared filters (Province, Brand, Country) ---
    with fcol1:
        all_provinces = sorted(df_raw["Province"].dropna().unique().tolist())
        sel_provinces = st.multiselect("Province", all_provinces, default=[])

    with fcol2:
        all_brands = sorted(df_raw["Brand"].dropna().unique().tolist())
        sel_brands = st.multiselect("Brand", all_brands, default=[])

    with fcol3:
        all_countries = sorted(df_raw["Country"].dropna().unique().tolist())
        sel_countries = st.multiselect("Country of Origin", all_countries, default=[])

    # --- View-specific filter ---
    with fcol4:
        if data_view == "By License Type":
            all_license_types = sorted(df_raw["License Type"].dropna().unique().tolist())
            sel_license_types = st.multiselect("License Type", all_license_types, default=[])
            sel_conditions = []
        else:
            all_conditions = sorted(df_raw["Condition"].dropna().unique().tolist())
            sel_conditions = st.multiselect("Condition", all_conditions, default=[])
            sel_license_types = []

    fcol5, fcol6, fcol7 = st.columns([1, 1, 2])
    
    with fcol5:
        all_fuels = sorted(df_raw["Fuel_Type"].dropna().unique().tolist())
        sel_fuels = st.multiselect("Fuel Type", all_fuels, default=[], key="mkt_fuel")
        
    with fcol6:
        all_shapes = sorted(df_raw["Shape"].dropna().unique().tolist())
        sel_shapes = st.multiselect("Shape", all_shapes, default=[], key="mkt_shape")
        
    with fcol7:
        st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
        top_n = st.slider("Top N in Charts", 5, 25, 15, key="mkt_topn",
                                   help="Control how many items appear in bar charts")

# ──────────────────────────────────────────────
# Apply Filters
# ──────────────────────────────────────────────
df = df_raw.copy()

if sel_provinces:
    df = df[df["Province"].isin(sel_provinces)]
if sel_brands:
    df = df[df["Brand"].isin(sel_brands)]
if sel_countries:
    df = df[df["Country"].isin(sel_countries)]

if data_view == "By License Type":
    if sel_license_types:
        df = df[df["License Type"].isin(sel_license_types)]
else:
    if sel_conditions:
        df = df[df["Condition"].isin(sel_conditions)]

if sel_fuels:
    df = df[df["Fuel_Type"].isin(sel_fuels)]
if sel_shapes:
    df = df[df["Shape"].isin(sel_shapes)]

# ──────────────────────────────────────────────
# Page Title
# ──────────────────────────────────────────────
st.markdown("## :material/pie_chart: Market Distribution & Conditions")
gold_divider()

# Handle empty data gracefully
if df.empty:
    st.warning("No data matches the selected filters. Please adjust your selections.")
    st.stop()

# ──────────────────────────────────────────────
# KPI Cards
# ──────────────────────────────────────────────
total_vehicles = int(df["Grand Total"].sum())
n_provinces = df["Province"].nunique()
n_brands = df["Brand"].nunique()

if data_view == "By License Type":
    specific_label = "License Types"
    specific_icon = "document"
    specific_count = df["License Type"].nunique()
else:
    specific_label = "Conditions"
    specific_icon = "tool"
    specific_count = df["Condition"].nunique()

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total Vehicles", f"{total_vehicles:,}", "car")
with k2:
    kpi_card("Provinces", f"{n_provinces:,}", "location")
with k3:
    kpi_card("Brands", f"{n_brands:,}", "brand")
with k4:
    kpi_card(specific_label, f"{specific_count:,}", specific_icon)

st.markdown("")

# ──────────────────────────────────────────────
# Row 1: Distribution Donut + Top 15 Brands
# ──────────────────────────────────────────────
section_header(":material/grid_view: Distribution Overview")
col_left, col_right = st.columns(2)

with col_left:
    if data_view == "By License Type":
        agg_type = (
            df.groupby("License Type", as_index=False)["Grand Total"]
            .sum()
            .sort_values("Grand Total", ascending=False)
        )
        treemap_chart(agg_type, path=["License Type"], values="Grand Total",
                    title="Distribution by License Type")
    else:
        agg_cond = (
            df.groupby("Condition", as_index=False)["Grand Total"]
            .sum()
            .sort_values("Grand Total", ascending=False)
        )
        treemap_chart(agg_cond, path=["Condition"], values="Grand Total",
                    title="Distribution by Vehicle Condition")

with col_right:
    agg_brand = (
        df.groupby("Brand", as_index=False)["Grand Total"]
        .sum()
        .sort_values("Grand Total", ascending=False)
        .head(top_n)
    )
    horizontal_bar(agg_brand, x="Grand Total", y="Brand",
                   title=f"Top {top_n} Brands by Volume", n=top_n)

# ──────────────────────────────────────────────
# Row 2: Full-width – Top Provinces (Stacked Bar)
# ──────────────────────────────────────────────
section_header(":material/map: Provincial Breakdown")

# Determine the color/category column
cat_col = "License Type" if data_view == "By License Type" else "Condition"

# Pre-aggregate: find top provinces first, then aggregate with category
top_provinces_list = (
    df.groupby("Province", as_index=False)["Grand Total"]
    .sum()
    .nlargest(top_n, "Grand Total")["Province"]
    .tolist()
)

agg_province = (
    df[df["Province"].isin(top_provinces_list)]
    .groupby(["Province", cat_col], as_index=False)["Grand Total"]
    .sum()
)

# Sort provinces by total for better visual ordering
province_order = (
    agg_province.groupby("Province")["Grand Total"]
    .sum()
    .sort_values(ascending=False)
    .index.tolist()
)
agg_province["Province"] = pd.Categorical(
    agg_province["Province"], categories=province_order, ordered=True
)
agg_province = agg_province.sort_values("Province")

stacked_bar(agg_province, x="Province", y="Grand Total", color=cat_col,
            title=f"Top {top_n} Provinces by {cat_col}", height=500)

# ──────────────────────────────────────────────
# Row 3: Country of Origin + Fuel Type Donuts
# ──────────────────────────────────────────────
section_header(":material/public: Global & Fuel Trends")
col_a, col_b = st.columns(2)

with col_a:
    agg_country = (
        df.groupby("Country", as_index=False)["Grand Total"]
        .sum()
        .sort_values("Grand Total", ascending=False)
    )
    horizontal_bar(agg_country, x="Grand Total", y="Country",
                title="Country of Origin Distribution", n=10)

with col_b:
    agg_fuel = (
        df.groupby("Fuel_Type", as_index=False)["Grand Total"]
        .sum()
        .sort_values("Grand Total", ascending=False)
    )
    donut_chart(agg_fuel, names="Fuel_Type", values="Grand Total",
                title="Fuel Type Distribution")

# ──────────────────────────────────────────────
# Data Table (first 1000 rows for performance)
# ──────────────────────────────────────────────
gold_divider()
section_header(":material/dataset: Raw Data Explorer")
data_table(df.head(1000), title="Filtered Data (first 1,000 rows)", height=450)
