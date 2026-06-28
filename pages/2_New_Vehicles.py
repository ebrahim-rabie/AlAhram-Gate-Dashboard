import streamlit as st
import pandas as pd

# --- Page Config (must be first Streamlit command) ---
st.set_page_config(page_title='New Vehicles | AlAhram', page_icon='assets/logo.png', layout='wide', initial_sidebar_state='collapsed')

from utils.theme import inject_custom_css, render_top_header, get_colors
from utils.charts import (
    kpi_card, section_header, gold_divider,
    donut_chart, horizontal_bar, treemap_chart, egypt_map_chart, data_table,
)
from utils.data_loader import load_new_vehicles, load_new_private

# --- Theme & Sidebar Header ---
inject_custom_css()
render_top_header()
colors = get_colors()

# ────────────────────────────────────────────
# Top Filters
# ────────────────────────────────────────────
with st.expander(":material/search: Search & Filters", expanded=False):
    view_mode = st.radio('View Mode', ['All New Vehicles', 'Private Only'], horizontal=True)
    
    # Load the appropriate dataset
    if view_mode == 'Private Only':
        raw_df = load_new_private()
    else:
        raw_df = load_new_vehicles()
    
    df = raw_df.copy() if raw_df is not None else pd.DataFrame()
    
    fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns(5)
    
    with fcol1:
        province_opts = sorted(df['Province'].dropna().unique().tolist()) if not df.empty else []
        sel_province = st.multiselect('Province', province_opts)
        
    with fcol2:
        # Filter df by province first to cascade traffic unit
        temp_df = df[df['Province'].isin(sel_province)] if sel_province else df
        tu_opts = sorted(temp_df['Traffic Unit'].dropna().unique().tolist()) if not temp_df.empty else []
        sel_traffic = st.multiselect('Traffic Unit', tu_opts, help='Auto-filtered by selected Province')
        
    with fcol3:
        brand_opts = sorted(df['Brand'].dropna().unique().tolist()) if not df.empty else []
        sel_brand = st.multiselect('Brand', brand_opts)
        
    with fcol4:
        country_opts = sorted(df['Country'].dropna().unique().tolist()) if not df.empty else []
        sel_country = st.multiselect('Country', country_opts)
        
    with fcol5:
        fuel_opts = sorted(df['Fuel_Type'].dropna().unique().tolist()) if not df.empty else []
        sel_fuel = st.multiselect('Fuel Type', fuel_opts)

    # Second row: Model filter
    fcol6, _ = st.columns([1, 4])
    with fcol6:
        model_opts = sorted(df['Model'].dropna().unique().tolist()) if not df.empty else []
        sel_model = st.multiselect('Model', model_opts)

# Guard against empty data
if raw_df is None or raw_df.empty:
    st.warning('⚠️ No data available for the selected view.')
    st.stop()

if sel_province:
    df = df[df['Province'].isin(sel_province)]
if sel_traffic:
    df = df[df['Traffic Unit'].isin(sel_traffic)]
if sel_brand:
    df = df[df['Brand'].isin(sel_brand)]
if sel_country:
    df = df[df['Country'].isin(sel_country)]
if sel_fuel:
    df = df[df['Fuel_Type'].isin(sel_fuel)]
if sel_model:
    df = df[df['Model'].isin(sel_model)]

# ────────────────────────────────────────────
# Empty-state guard after filtering
# ────────────────────────────────────────────
if df.empty:
    st.warning('⚠️ No records match the selected filters. Please adjust your criteria.')
    st.stop()

# ────────────────────────────────────────────
# Page Title
# ────────────────────────────────────────────
st.markdown(f"## :material/fiber_new: New Vehicles Market")
subtitle = 'Private Vehicles Only' if view_mode == 'Private Only' else 'All New Vehicles'
st.caption(f'Showing: **{subtitle}** — {len(df):,} records')
gold_divider()

# ────────────────────────────────────────────
# KPI Cards
# ────────────────────────────────────────────
total_registrations = int(df['Grand Total'].sum())

# Top Province
prov_totals = df.groupby('Province', as_index=False)['Grand Total'].sum()
top_province = prov_totals.loc[prov_totals['Grand Total'].idxmax(), 'Province'] if not prov_totals.empty else '—'

# Top Brand
brand_totals = df.groupby('Brand', as_index=False)['Grand Total'].sum()
top_brand = brand_totals.loc[brand_totals['Grand Total'].idxmax(), 'Brand'] if not brand_totals.empty else '—'

# Fuel types count
fuel_count = df['Fuel_Type'].nunique()

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card('Total Registrations', f'{total_registrations:,}', 'car')
with k2:
    kpi_card('Top Province', top_province, 'location')
with k3:
    kpi_card('Top Brand', top_brand, 'trophy')
with k4:
    kpi_card('Fuel Types', str(fuel_count), 'fuel')

gold_divider()

# ────────────────────────────────────────────
# Section 1: Top 15 Brands (full width)
# ────────────────────────────────────────────
section_header(':material/factory: Top 15 Brands')
brand_df = (
    df.groupby('Brand', as_index=False)['Grand Total']
    .sum()
    .sort_values('Grand Total', ascending=False)
    .head(15)
)
horizontal_bar(brand_df, x='Grand Total', y='Brand', title='Top 15 Brands by Registrations', n=15)

gold_divider()

# ────────────────────────────────────────────
# Section: Top 15 Models
# ────────────────────────────────────────────
section_header(':material/model_training: Top 15 Models')
model_df = (
    df.groupby('Model', as_index=False)['Grand Total']
    .sum()
    .sort_values('Grand Total', ascending=False)
    .head(15)
)
horizontal_bar(model_df, x='Grand Total', y='Model', title='Top 15 Models by Registrations', n=15)

gold_divider()

# ────────────────────────────────────────────
# Section 2: Provinces + Fuel Type
# ────────────────────────────────────────────
section_header(':material/map: Provincial Distribution & Fuel Types')
col_a, col_b = st.columns(2)

with col_a:
    prov_df = (
        df.groupby('Province', as_index=False)['Grand Total']
        .sum()
        .sort_values('Grand Total', ascending=False)
    )
    egypt_map_chart(prov_df, prov_col='Province', val_col='Grand Total', title='Provincial Distribution Map', height=450)

with col_b:
    fuel_df = (
        df.groupby('Fuel_Type', as_index=False)['Grand Total']
        .sum()
        .sort_values('Grand Total', ascending=False)
    )
    donut_chart(fuel_df, names='Fuel_Type', values='Grand Total', title='Fuel Type Distribution')

gold_divider()

# ────────────────────────────────────────────
# Section 3: Traffic Units + Country Treemap
# ────────────────────────────────────────────
section_header(':material/public: Traffic Units & Country of Origin')
col_c, col_d = st.columns(2)

with col_c:
    tu_df = (
        df.groupby('Traffic Unit', as_index=False)['Grand Total']
        .sum()
        .sort_values('Grand Total', ascending=False)
        .head(10)
    )
    horizontal_bar(tu_df, x='Grand Total', y='Traffic Unit', title='Top 10 Traffic Units', n=10)

with col_d:
    country_df = (
        df.groupby('Country', as_index=False)['Grand Total']
        .sum()
        .sort_values('Grand Total', ascending=False)
    )
    # Filter out zero / negative values for treemap
    country_df = country_df[country_df['Grand Total'] > 0]
    treemap_chart(country_df, path=['Country'], values='Grand Total', title='Country of Origin')

gold_divider()

# ────────────────────────────────────────────
# Data Table
# ────────────────────────────────────────────
section_header(':material/dataset: Detailed Data')
data_table(df, title='New Vehicles — Raw Data')
