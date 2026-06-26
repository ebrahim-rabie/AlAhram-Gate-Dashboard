"""
AlAhram Gate Dashboard — Page 2: Electric Vehicles Analysis
Comprehensive analysis of electric vehicle registrations by license type,
brand, country, shape, and fuel sub-type.
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="EV Analysis | AlAhram", page_icon="assets/logo.png", layout="wide", initial_sidebar_state="collapsed")

from utils.theme import inject_custom_css, render_top_header, get_colors
from utils.charts import (
    kpi_card,
    section_header,
    gold_divider,
    donut_chart,
    horizontal_bar,
    treemap_chart,
    data_table,
)
from utils.data_loader import load_ev_by_license, load_ev_january

# ── Theme Setup ─────────────────────────────────────────────────────────────
inject_custom_css()
render_top_header()

# ── Load Data ───────────────────────────────────────────────────────────────
ev_df = load_ev_by_license()
ev_jan_df = load_ev_january()

# ── Top Filters ─────────────────────────────────────────────────────────
with st.expander(":material/search: Search & Filters", expanded=False):
    fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns(5)
    
    with fcol1:
        brands = sorted(ev_df["Brand"].dropna().unique().tolist())
        selected_brands = st.multiselect("Brand", brands, default=[], key="ev_brand")
        
    with fcol2:
        countries = sorted(ev_df["Country"].dropna().unique().tolist())
        selected_countries = st.multiselect("Country", countries, default=[], key="ev_country")
        
    with fcol3:
        shapes = sorted(ev_df["Shape"].dropna().unique().tolist())
        selected_shapes = st.multiselect("Shape", shapes, default=[], key="ev_shape")
        
    with fcol4:
        fuel_types = sorted(ev_df["Fuel_Type"].dropna().unique().tolist())
        selected_fuel_types = st.multiselect("Fuel Type", fuel_types, default=[], key="ev_fuel")
        
    with fcol5:
        min_regs = st.number_input("Min Registrations", min_value=0, value=0, step=5, key="ev_min_regs",
                                    help="Hide brands with fewer than N total registrations")

# ── Apply Filters ───────────────────────────────────────────────────────────
filtered_df = ev_df.copy()

if selected_brands:
    filtered_df = filtered_df[filtered_df["Brand"].isin(selected_brands)]
if selected_countries:
    filtered_df = filtered_df[filtered_df["Country"].isin(selected_countries)]
if selected_shapes:
    filtered_df = filtered_df[filtered_df["Shape"].isin(selected_shapes)]
if selected_fuel_types:
    filtered_df = filtered_df[filtered_df["Fuel_Type"].isin(selected_fuel_types)]
if min_regs > 0 and "Grand Total" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Grand Total"] >= min_regs]

# ── Page Title ──────────────────────────────────────────────────────────────
st.markdown("# :material/electric_car: Electric Vehicles Analysis")
gold_divider()

# ── KPI Cards ───────────────────────────────────────────────────────────────
total_evs = int(filtered_df["Grand Total"].sum()) if not filtered_df.empty else 0

# Top brand by Grand Total
if not filtered_df.empty and "Brand" in filtered_df.columns:
    brand_totals = filtered_df.groupby("Brand")["Grand Total"].sum()
    top_brand = brand_totals.idxmax() if not brand_totals.empty else "N/A"
else:
    top_brand = "N/A"

# Unique countries in filtered data
countries_count = filtered_df["Country"].dropna().nunique() if not filtered_df.empty else 0

# January 2026 total (from ev_january df, unfiltered – it's a spotlight)
jan_total = int(ev_jan_df["Grand Total"].sum()) if not ev_jan_df.empty else 0

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Total EVs", total_evs, "electric")
with k2:
    kpi_card("Top Brand", top_brand, "trophy")
with k3:
    kpi_card("Countries", countries_count, "world")
with k4:
    kpi_card("Jan 2026 Total", jan_total, "calendar")

st.markdown("")

# ── Top 15 EV Brands (Full Width) ──────────────────────────────────────────
section_header(":material/factory: Top 15 EV Brands")

if not filtered_df.empty:
    brand_df = (
        filtered_df.groupby("Brand")["Grand Total"]
        .sum()
        .reset_index()
        .rename(columns={"Grand Total": "Total"})
    )
    horizontal_bar(brand_df, x="Total", y="Brand", title="Top 15 Electric Vehicle Brands", n=15, height=500)
else:
    st.info("No data available for the selected filters.")

gold_divider()

# ── License Type Distribution & Country of Origin ──────────────────────────
LICENSE_TYPES = [
    "Private", "motorcycle", "Public bus", "transfer",
    "Temporary license", "Private bus", "Commercial",
    "Customs Private", "Tourist", "Diplomatic body",
    "Tourism bus", "Trips", "Motorbike", "Heavy Transport",
    "School bus", "Customs bus", "Suspended",
]

col_left, col_right = st.columns(2)

with col_left:
    section_header(":material/list_alt: License Type Distribution")
    if not filtered_df.empty:
        # Aggregate across all license type columns
        available_types = [lt for lt in LICENSE_TYPES if lt in filtered_df.columns]
        if available_types:
            license_sums = {lt: filtered_df[lt].sum() for lt in available_types}
            license_df = pd.DataFrame(
                list(license_sums.items()),
                columns=["License Type", "Count"],
            )
            # Keep only non-zero for cleaner chart
            license_df = license_df[license_df["Count"] > 0].sort_values("Count", ascending=False)
            if not license_df.empty:
                horizontal_bar(license_df, x="Count", y="License Type",
                            title="EV Distribution by License Type", height=450, n=15)
            else:
                st.info("No license type data available.")
        else:
            st.info("License type columns not found in data.")
    else:
        st.info("No data available for the selected filters.")

with col_right:
    section_header(":material/public: Country of Origin")
    if not filtered_df.empty:
        country_df = (
            filtered_df.groupby("Country")["Grand Total"]
            .sum()
            .reset_index()
            .rename(columns={"Grand Total": "Total"})
            .sort_values("Total", ascending=False)
        )
        if not country_df.empty:
            treemap_chart(country_df, path=["Country"], values="Total",
                        title="EVs by Country of Origin", height=450)
        else:
            st.info("No country data available.")
    else:
        st.info("No data available for the selected filters.")

gold_divider()

# ── Vehicle Shape & Fuel Sub-Type ──────────────────────────────────────────
col_shape, col_fuel = st.columns(2)

with col_shape:
    section_header(":material/directions_car: Vehicle Shape")
    if not filtered_df.empty:
        shape_df = (
            filtered_df.groupby("Shape")["Grand Total"]
            .sum()
            .reset_index()
            .rename(columns={"Grand Total": "Total"})
            .sort_values("Total", ascending=False)
        )
        if not shape_df.empty:
            horizontal_bar(shape_df, x="Total", y="Shape",
                        title="EVs by Vehicle Shape", height=450, n=10)
        else:
            st.info("No shape data available.")
    else:
        st.info("No data available for the selected filters.")

with col_fuel:
    section_header(":material/local_gas_station: Fuel Sub-Type")
    if not filtered_df.empty:
        fuel_df = (
            filtered_df.groupby("Fuel_Type")["Grand Total"]
            .sum()
            .reset_index()
            .rename(columns={"Grand Total": "Total"})
            .sort_values("Total", ascending=False)
        )
        if not fuel_df.empty:
            donut_chart(fuel_df, names="Fuel_Type", values="Total",
                        title="EVs by Fuel Sub-Type", height=450)
        else:
            st.info("No fuel type data available.")
    else:
        st.info("No data available for the selected filters.")

gold_divider()

# ── January 2026 Spotlight ──────────────────────────────────────────────────
section_header(":material/calendar_month: January 2026 Spotlight")

if not ev_jan_df.empty:
    # Top 10 brands from January data
    jan_top = (
        ev_jan_df.groupby("Brand")["Grand Total"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
        .rename(columns={"Grand Total": "Jan 2026 Total"})
    )

    colors = get_colors()

    # Style the dataframe with highlights
    st.markdown(
        f"""
        <div style="
            background: {colors['bg_card']};
            border: 1px solid {colors['border']};
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        ">
            <h4 style="color: {colors['accent_gold']}; margin-bottom: 10px;">
                Top 10 EV Brands — January 2026
            </h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        jan_top.style
        .background_gradient(subset=["Jan 2026 Total"], cmap="YlOrRd")
        .format({"Jan 2026 Total": "{:,.0f}"}),
        use_container_width=True,
        hide_index=True,
        height=400,
    )
else:
    st.info("January 2026 data is not available.")

gold_divider()

# ── Full Data Table ─────────────────────────────────────────────────────────
data_table(filtered_df, title=":material/dataset: Electric Vehicles — Full Data Explorer", height=500)
