import streamlit as st
import pandas as pd

# ── Page config (must be first Streamlit command) ──
st.set_page_config(page_title="Specs | AlAhram", page_icon="assets/logo.png", layout="wide", initial_sidebar_state="collapsed")

from utils.theme import inject_custom_css, render_top_header, get_colors
from utils.charts import (
    kpi_card, section_header, gold_divider,
    donut_chart, horizontal_bar, heatmap_chart,
    histogram_chart, box_plot, egypt_map_chart, data_table,
)
from utils.data_loader import load_shape_engine, load_private_by_gov

# ── Theme & sidebar ──
inject_custom_css()
render_top_header()
colors = get_colors()

# ── Load data ──
df_shape = load_shape_engine()
df_gov = load_private_by_gov()

# ══════════════════════════════════════════════════════════════
# Top Filters
# ══════════════════════════════════════════════════════════════
with st.expander(":material/search: Search & Filters", expanded=False):
    fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns(5)
    
    with fcol1:
        # Brand filter (from shape_engine)
        all_brands = sorted(df_shape["Brand"].dropna().unique().tolist())
        sel_brands = st.multiselect("Brand", all_brands, default=[])
    
    with fcol2:
        # Body Shape filter
        all_shapes = sorted(df_shape["Body Shape"].dropna().unique().tolist())
        sel_shapes = st.multiselect("Body Shape", all_shapes, default=[])
    
    with fcol3:
        # Province filter (from gov df)
        all_provinces = sorted(df_gov["Province"].dropna().unique().tolist())
        sel_provinces = st.multiselect("Province", all_provinces, default=[])
    
    with fcol4:
        # Fuel Type filter (union of both dataframes)
        fuel_vals = set(
            df_shape["Fuel_Type"].dropna().unique().tolist()
            + df_gov["Fuel_Type"].dropna().unique().tolist()
        )
        all_fuels = sorted(fuel_vals)
        sel_fuels = st.multiselect("Fuel Type", all_fuels, default=[])

# ── Apply filters ──
if sel_brands:
    df_shape = df_shape[df_shape["Brand"].isin(sel_brands)]
    df_gov = df_gov[df_gov["Brand"].isin(sel_brands)]

if sel_shapes:
    df_shape = df_shape[df_shape["Body Shape"].isin(sel_shapes)]

if sel_provinces:
    df_gov = df_gov[df_gov["Province"].isin(sel_provinces)]

if sel_fuels:
    df_shape = df_shape[df_shape["Fuel_Type"].isin(sel_fuels)]
    df_gov = df_gov[df_gov["Fuel_Type"].isin(sel_fuels)]

# Country filter
    all_countries = sorted(set(
        df_shape["Country"].dropna().unique().tolist()
        + df_gov["Country"].dropna().unique().tolist()
    ))
    with fcol5:
        sel_countries = st.multiselect("Country", all_countries, default=[])
    
    if sel_countries:
        df_shape = df_shape[df_shape["Country"].isin(sel_countries)]
        df_gov = df_gov[df_gov["Country"].isin(sel_countries)]
    
    # Engine CC Range slider
    st.markdown("---")
    if not df_shape.empty and "Engine CC" in df_shape.columns and df_shape["Engine CC"].notna().any():
        min_cc = int(df_shape["Engine CC"].min())
        max_cc = int(df_shape["Engine CC"].max())
        if min_cc < max_cc:
            cc_range = st.slider("Engine CC Range", min_cc, max_cc, (min_cc, max_cc),
                                          help="Filter by engine capacity in cubic centimeters")
            df_shape = df_shape[(df_shape["Engine CC"] >= cc_range[0]) & (df_shape["Engine CC"] <= cc_range[1])]

# ══════════════════════════════════════════════════════════════
# Page Title
# ══════════════════════════════════════════════════════════════
st.markdown("## :material/build: Vehicle Specifications")
gold_divider()

# ══════════════════════════════════════════════════════════════
# KPI Row
# ══════════════════════════════════════════════════════════════
unique_shapes = df_shape["Body Shape"].nunique() if not df_shape.empty else 0
avg_engine = int(df_shape["Engine CC"].mean()) if not df_shape.empty and df_shape["Engine CC"].notna().any() else 0

if not df_gov.empty:
    top_province = df_gov.groupby("Province")["Count"].sum().idxmax()
else:
    top_province = "N/A"

if not df_shape.empty:
    top_body = df_shape.groupby("Body Shape")["Count"].sum().idxmax()
else:
    top_body = "N/A"

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Unique Shapes", f"{unique_shapes}", "car")
with k2:
    kpi_card("Avg Engine CC", f"{avg_engine:,}", "engine")
with k3:
    kpi_card("Top Province", top_province, "location")
with k4:
    kpi_card("Top Body Type", top_body, "car")

st.markdown("")

# ══════════════════════════════════════════════════════════════
# Row 1: Body Shape Donut + Engine CC Histogram
# ══════════════════════════════════════════════════════════════
section_header(":material/bar_chart: Shape & Engine Overview")
col1, col2 = st.columns(2)

with col1:
    if not df_shape.empty:
        shape_dist = (
            df_shape.groupby("Body Shape", as_index=False)["Count"]
            .sum()
            .sort_values("Count", ascending=False)
        )
        horizontal_bar(shape_dist, x="Count", y="Body Shape", title="Body Shape Distribution", n=10)
    else:
        st.info("No data available for Body Shape distribution.")

with col2:
    if not df_shape.empty and df_shape["Engine CC"].notna().any():
        histogram_chart(df_shape, x="Engine CC", title="Engine CC Distribution", nbins=30)
    else:
        st.info("No data available for Engine CC distribution.")

st.markdown("")

# ══════════════════════════════════════════════════════════════
# Row 2: Brand × Shape Heatmap (full width)
# ══════════════════════════════════════════════════════════════
section_header(":material/grid_on: Brand × Body Shape Heatmap")

if not df_shape.empty:
    # Limit to top 15 brands by total count
    brand_totals = df_shape.groupby("Brand")["Count"].sum().nlargest(15).index.tolist()
    heatmap_df = (
        df_shape[df_shape["Brand"].isin(brand_totals)]
        .groupby(["Brand", "Body Shape"], as_index=False)["Count"]
        .sum()
    )
    heatmap_chart(heatmap_df, x="Body Shape", y="Brand", z="Count", title="Brand × Body Shape (Top 15 Brands)")
else:
    st.info("No data available for heatmap.")

st.markdown("")

# ══════════════════════════════════════════════════════════════
# Row 3: Top Governorates + Engine CC by Brand Box Plot
# ══════════════════════════════════════════════════════════════
section_header(":material/map: Regional & Engine Analysis")
col3, col4 = st.columns(2)

with col3:
    if not df_gov.empty:
        gov_agg = (
            df_gov.groupby("Province", as_index=False)["Count"]
            .sum()
            .sort_values("Count", ascending=False)
        )
        egypt_map_chart(gov_agg, prov_col="Province", val_col="Count", title="Governorates Distribution Map", height=450)
    else:
        st.info("No data available for governorate distribution.")

with col4:
    if not df_shape.empty and df_shape["Engine CC"].notna().any():
        # Top 10 brands for box plot
        top10 = df_shape.groupby("Brand")["Count"].sum().nlargest(10).index.tolist()
        box_df = df_shape[df_shape["Brand"].isin(top10)]
        if not box_df.empty:
            box_plot(box_df, x="Brand", y="Engine CC", title="Engine CC by Brand (Top 10)")
        else:
            st.info("No data available for box plot.")
    else:
        st.info("No data available for Engine CC box plot.")

st.markdown("")

# ══════════════════════════════════════════════════════════════
# Data Table
# ══════════════════════════════════════════════════════════════
gold_divider()
section_header(":material/dataset: Raw Data – Shape & Engine")
data_table(df_shape, title="Vehicle Specifications Data")
