"""
AlAhram Gate Dashboard — Data Loader
Cached loading and cleaning of all 9 dataset files.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# ── Data Directory ──────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).parent.parent / "Dataset" / "DATA AFTER FUEL TYPE"

# ── File Paths ──────────────────────────────────────────────────────────────

FILES = {
    "ev_license": DATA_DIR / "Copy of fuel_after_map_english_إحصائية ماركات المركبات الكهربائية وفقاً لأنواع التراخيص.csv",
    "new_vehicles": DATA_DIR / "Copy of fuel_after_map_output_english_إحصائية الماركات والطرازات للمركبات الزيرو.csv",
    "new_private": DATA_DIR / "Copy of fuel_after_map_output_english_إحصائية الماركات والطرازات للملاكي الزيرو.xlsx",
    "license_condition_gov": DATA_DIR / "Copy of fuel_after_map_output_english_إحصائية الماركات والطرازات وفقاً لنوع الترخيص وحالة المركبة موزعة على محافظات الجمهورية (2).xlsx",
    "vehicle_condition": DATA_DIR / "Copy of fuel_after_map_output_englishإحصائية الماركات والطرازات وفقاً لحالة المركبة.xlsx",
    "shape_engine": DATA_DIR / "Copy of fuel_after_map_إحصائية الماركات للملاكي الزيرو وفقاً للشكل والسعة اللتريةclean.xlsx",
    "private_by_gov": DATA_DIR / "Copy of fuel_after_map_إحصائية الماركات والطرازات للملاكي الزيرو وفقاً للمحافظاتclean.xlsx",
    "ev_january": DATA_DIR / "Copy of fuel_after_map_إحصائية ماركات المركبات الكهربائية وفقاً لأنواع التراخيص عن شهر 01-2026clean.xlsx",
    "used_vehicles": DATA_DIR / "fuel_after_map_output_english_إحصائية الماركات والطرازات للمركبات الـUsed.xlsx",
}

# ── Column Renaming ─────────────────────────────────────────────────────────

COLUMN_RENAMES = {
    "my angel": "Private",
    "malaki": "Private",
    "Heavy stomach": "Heavy Transport",
    "brick": "Commercial",
    "Turn off": "Suspended",
    "Malaki customs": "Customs Private",
    "Tourist fare": "Tourist",
    "Motorbike fare": "Motorbike",
    "General total": "Grand Total",
    "port": "Traffic Unit",
    "Issuance province": "Province",
    "Year of manufacture": "Year",
    "Figure": "Body Shape",
    "Liter capacity": "Engine CC",
    "Number of vehicles": "Count",
    "M": "Row #",
    "Vehicle condition": "Condition",
    "License type": "License Type",
}

LICENSE_TYPES = [
    "Private", "motorcycle", "Public bus", "transfer",
    "Temporary license", "Private bus", "Commercial",
    "Customs Private", "Tourist", "Diplomatic body",
    "Tourism bus", "Trips", "Motorbike", "Heavy Transport",
    "School bus", "Customs bus", "Suspended",
]

YEAR_COLUMNS = [2022, 2023, 2024, 2025, 2026]


# ── Cleaning Helpers ────────────────────────────────────────────────────────

def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns using the standard mapping."""
    df = df.rename(columns=COLUMN_RENAMES)
    # Also handle float year column names (from Excel: 2022.0 -> 2022)
    rename_years = {}
    for col in df.columns:
        if isinstance(col, float) and col in [2022.0, 2023.0, 2024.0, 2025.0, 2026.0]:
            rename_years[col] = int(col)
    if rename_years:
        df = df.rename(columns=rename_years)
    return df


def _forward_fill_province(df: pd.DataFrame) -> pd.DataFrame:
    """Forward-fill merged-cell Province values."""
    if "Province" in df.columns:
        df["Province"] = df["Province"].ffill()
    return df


def _drop_unnamed(df: pd.DataFrame) -> pd.DataFrame:
    """Drop unnamed columns."""
    unnamed_cols = [c for c in df.columns if str(c).startswith("Unnamed")]
    return df.drop(columns=unnamed_cols, errors="ignore")


def _clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from string columns."""
    str_cols = df.select_dtypes(include=["object"]).columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": None, "None": None, "": None})
    return df


def _drop_total_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove grand total / summary rows."""
    if "Brand" in df.columns:
        df = df[df["Brand"].notna()]
        df = df[~df["Brand"].str.lower().isin(["grand total", "total", "الإجمالي الكلي"])]
    return df


# ── Individual Loaders ──────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def load_ev_by_license() -> pd.DataFrame:
    """Load electric vehicle brands by license type (File 1)."""
    df = pd.read_csv(FILES["ev_license"])
    df = _clean_columns(df)
    df = _drop_unnamed(df)
    df = _drop_total_rows(df)
    df = _clean_strings(df)
    # Fill NaN in license type columns with 0
    for col in LICENSE_TYPES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    if "Grand Total" in df.columns:
        df["Grand Total"] = pd.to_numeric(df["Grand Total"], errors="coerce").fillna(0)
    return df.reset_index(drop=True)


@st.cache_data(ttl=3600)
def load_ev_january() -> pd.DataFrame:
    """Load electric vehicle brands for January 2026 (File 8)."""
    df = pd.read_excel(FILES["ev_january"])
    df = _clean_columns(df)
    df = _drop_unnamed(df)
    df = _drop_total_rows(df)
    df = _clean_strings(df)
    for col in LICENSE_TYPES:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    if "Grand Total" in df.columns:
        df["Grand Total"] = pd.to_numeric(df["Grand Total"], errors="coerce").fillna(0)
    return df.reset_index(drop=True)


@st.cache_data(ttl=3600)
def load_new_vehicles() -> pd.DataFrame:
    """Load zero/new vehicle brands by location (File 2)."""
    df = pd.read_csv(FILES["new_vehicles"])
    df = _clean_columns(df)
    df = _drop_unnamed(df)
    df = _forward_fill_province(df)
    df = _drop_total_rows(df)
    df = _clean_strings(df)
    if "Grand Total" in df.columns:
        df["Grand Total"] = pd.to_numeric(df["Grand Total"], errors="coerce").fillna(0)
    return df.reset_index(drop=True)


@st.cache_data(ttl=3600)
def load_new_private() -> pd.DataFrame:
    """Load new private (ملاكي) vehicle brands (File 3)."""
    df = pd.read_excel(FILES["new_private"])
    df = _clean_columns(df)
    df = _drop_unnamed(df)
    df = _forward_fill_province(df)
    df = _drop_total_rows(df)
    df = _clean_strings(df)
    if "Grand Total" in df.columns:
        df["Grand Total"] = pd.to_numeric(df["Grand Total"], errors="coerce").fillna(0)
    return df.reset_index(drop=True)


@st.cache_data(ttl=3600)
def load_license_condition_gov() -> pd.DataFrame:
    """Load brands by license type, condition & governorate (File 4)."""
    df = pd.read_excel(FILES["license_condition_gov"])
    df = _clean_columns(df)
    df = _drop_unnamed(df)
    df = _forward_fill_province(df)
    df = _drop_total_rows(df)
    df = _clean_strings(df)
    if "Grand Total" in df.columns:
        df["Grand Total"] = pd.to_numeric(df["Grand Total"], errors="coerce").fillna(0)
    # Forward fill License Type as well (merged cells)
    if "License Type" in df.columns:
        df["License Type"] = df["License Type"].ffill()
    return df.reset_index(drop=True)


@st.cache_data(ttl=3600)
def load_vehicle_condition() -> pd.DataFrame:
    """Load brands by vehicle condition (File 5)."""
    df = pd.read_excel(FILES["vehicle_condition"])
    df = _clean_columns(df)
    df = _drop_unnamed(df)
    df = _forward_fill_province(df)
    df = _drop_total_rows(df)
    df = _clean_strings(df)
    if "Grand Total" in df.columns:
        df["Grand Total"] = pd.to_numeric(df["Grand Total"], errors="coerce").fillna(0)
    # Forward fill Traffic Unit and Condition (merged cells)
    if "Traffic Unit" in df.columns:
        df["Traffic Unit"] = df["Traffic Unit"].ffill()
    if "Condition" in df.columns:
        df["Condition"] = df["Condition"].ffill()
    return df.reset_index(drop=True)


@st.cache_data(ttl=3600)
def load_shape_engine() -> pd.DataFrame:
    """Load private zero by shape & engine capacity (File 6)."""
    df = pd.read_excel(FILES["shape_engine"])
    df = _clean_columns(df)
    df = _drop_unnamed(df)
    df = _drop_total_rows(df)
    df = _clean_strings(df)
    if "Count" in df.columns:
        df["Count"] = pd.to_numeric(df["Count"], errors="coerce").fillna(0)
    if "Engine CC" in df.columns:
        df["Engine CC"] = pd.to_numeric(df["Engine CC"], errors="coerce").fillna(0)
    return df.reset_index(drop=True)


@st.cache_data(ttl=3600)
def load_private_by_gov() -> pd.DataFrame:
    """Load private zero brands by governorate (File 7)."""
    df = pd.read_excel(FILES["private_by_gov"])
    df = _clean_columns(df)
    df = _drop_unnamed(df)
    df = _forward_fill_province(df)
    df = _drop_total_rows(df)
    df = _clean_strings(df)
    if "Count" in df.columns:
        df["Count"] = pd.to_numeric(df["Count"], errors="coerce").fillna(0)
    return df.reset_index(drop=True)


@st.cache_data(ttl=3600)
def load_used_vehicles() -> pd.DataFrame:
    """Load used vehicle brands & models (File 9)."""
    df = pd.read_excel(FILES["used_vehicles"])
    df = _clean_columns(df)
    df = _forward_fill_province(df)
    df = _drop_total_rows(df)
    df = _clean_strings(df)
    # Keep year columns (2022-2026) and fill NaN with 0
    for yr in YEAR_COLUMNS:
        if yr in df.columns:
            df[yr] = pd.to_numeric(df[yr], errors="coerce").fillna(0)
    if "Grand Total" in df.columns:
        df["Grand Total"] = pd.to_numeric(df["Grand Total"], errors="coerce").fillna(0)
    # Drop unnamed columns but keep year columns
    unnamed_cols = [c for c in df.columns if str(c).startswith("Unnamed")]
    df = df.drop(columns=unnamed_cols, errors="ignore")
    return df.reset_index(drop=True)


# ── Aggregate Summary ──────────────────────────────────────────────────────

@st.cache_data(ttl=3600)
def load_all_summary() -> dict:
    """Load aggregated KPIs from all datasets."""
    ev = load_ev_by_license()
    new = load_new_vehicles()
    used = load_used_vehicles()
    ev_jan = load_ev_january()

    total_ev = int(ev["Grand Total"].sum()) if "Grand Total" in ev.columns else 0
    total_new = int(new["Grand Total"].sum()) if "Grand Total" in new.columns else 0
    total_used = int(used["Grand Total"].sum()) if "Grand Total" in used.columns else 0

    # Unique brands across all datasets
    all_brands = set()
    for df in [ev, new, used]:
        if "Brand" in df.columns:
            all_brands.update(df["Brand"].dropna().unique())

    # Unique countries
    all_countries = set()
    for df in [ev, new, used]:
        if "Country" in df.columns:
            all_countries.update(df["Country"].dropna().unique())

    # Top brands from new vehicles
    top_brands = pd.DataFrame()
    if "Brand" in new.columns and "Grand Total" in new.columns:
        top_brands = (
            new.groupby("Brand")["Grand Total"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

    # Fuel type distribution from new vehicles
    fuel_dist = pd.DataFrame()
    if "Fuel_Type" in new.columns and "Grand Total" in new.columns:
        fuel_dist = (
            new.groupby("Fuel_Type")["Grand Total"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

    # Country distribution
    country_dist = pd.DataFrame()
    if "Country" in new.columns and "Grand Total" in new.columns:
        country_dist = (
            new.groupby("Country")["Grand Total"]
            .sum()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )

    # Year trend from used vehicles
    year_trend = pd.DataFrame()
    year_cols = [c for c in used.columns if c in YEAR_COLUMNS]
    if year_cols:
        year_sums = {yr: used[yr].sum() for yr in year_cols}
        year_trend = pd.DataFrame(
            list(year_sums.items()), columns=["Year", "Registrations"]
        )

    return {
        "total_ev": total_ev,
        "total_new": total_new,
        "total_used": total_used,
        "total_all": total_ev + total_new + total_used,
        "total_brands": len(all_brands),
        "total_countries": len(all_countries),
        "ev_jan_total": int(ev_jan["Grand Total"].sum()) if "Grand Total" in ev_jan.columns else 0,
        "top_brands": top_brands,
        "fuel_dist": fuel_dist,
        "country_dist": country_dist,
        "year_trend": year_trend,
    }
