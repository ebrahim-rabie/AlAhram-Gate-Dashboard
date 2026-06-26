# 🏛️ AlAhram Gate Dashboard — Full Streamlit Implementation Plan

> **Language:** English | **Theme:** Dark + Light Mode | **Framework:** Streamlit Multipage App

---

## 📁 Complete File Architecture

```
AlAhram-Gate-Dashboard/
│
├── 🏠 app.py                              ← Home / Overview (Page 1)
│
├── 📄 pages/
│   ├── 1_⚡_Electric_Vehicles.py           ← Page 2: EV Analysis
│   ├── 2_🆕_New_Vehicles.py                ← Page 3: New Cars Market
│   ├── 3_🔧_Vehicle_Specs.py               ← Page 4: Specifications
│   ├── 4_📊_Market_Distribution.py         ← Page 5: License & Condition
│   └── 5_🔄_Used_Vehicles.py               ← Page 6: Used Cars Market
│
├── 📦 utils/
│   ├── __init__.py
│   ├── data_loader.py                      ← Cached data loading + cleaning
│   ├── theme.py                            ← Dual color palettes + chart configs
│   └── charts.py                           ← Reusable Plotly chart builders
│
├── 🎨 .streamlit/
│   └── config.toml                         ← Streamlit theme config
│
├── 🖼️ assets/
│   └── logo.png                            ← Al-Ahram logo (existing)
│
├── 📁 Dataset/                             ← Existing data files (9 files)
│
├── 📋 requirements.txt
└── 📖 README.md
```

**Total files to create: 13 new files**

---

## 🎨 Dual Theme System (Dark + Light)

### Dark Mode Palette

| Token | Hex | Role |
|-------|-----|------|
| `bg_primary` | `#0E1117` | Page background |
| `bg_secondary` | `#262730` | Cards, sidebar |
| `bg_card` | `#1E1E2E` | Metric cards, chart containers |
| `text_primary` | `#FFFFFF` | Main text |
| `text_secondary` | `#B0B0B0` | Muted text, labels |
| `accent_red` | `#C8102E` | Al-Ahram Red — primary accent |
| `accent_gold` | `#D4A84B` | Pyramid Gold — secondary accent |
| `accent_bright` | `#F0B429` | Highlights, positive deltas |
| `border` | `#3A3A4A` | Card borders, dividers |

### Light Mode Palette

| Token | Hex | Role |
|-------|-----|------|
| `bg_primary` | `#FFFFFF` | Page background |
| `bg_secondary` | `#F5F5F5` | Cards, sidebar |
| `bg_card` | `#FAFAFA` | Metric cards, chart containers |
| `text_primary` | `#1A1A1A` | Main text |
| `text_secondary` | `#666666` | Muted text, labels |
| `accent_red` | `#C8102E` | Al-Ahram Red — primary accent |
| `accent_gold` | `#D4A84B` | Pyramid Gold — secondary accent |
| `accent_bright` | `#B8860B` | Highlights (darker gold for contrast) |
| `border` | `#E0E0E0` | Card borders, dividers |

### Chart Colors (shared across both themes)

```python
CHART_COLORS = [
    "#C8102E",  # Al-Ahram Red
    "#D4A84B",  # Pyramid Gold
    "#F0B429",  # Accent Gold
    "#4ECDC4",  # Teal
    "#45B7D1",  # Sky Blue
    "#FF6B6B",  # Coral
    "#96CEB4",  # Sage Green
    "#DDA0DD",  # Plum
    "#FF8C42",  # Tangerine
    "#6C5CE7",  # Purple
]
```

---

## 📦 File-by-File Implementation

---

### 1. `.streamlit/config.toml` — Streamlit Theme Config

```toml
[theme]
primaryColor = "#C8102E"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FFFFFF"
font = "sans serif"

[server]
headless = true
```

> [!NOTE]
> Streamlit's built-in theme toggle (☀️/🌙 in the settings menu) will switch between our custom dark theme and the default light theme. We'll also add a **manual toggle** in the sidebar for convenience.

---

### 2. `requirements.txt` — Dependencies

```
streamlit>=1.28
pandas>=2.0
openpyxl>=3.1
plotly>=5.18
```

---

### 3. `utils/__init__.py`

```python
# Empty — makes utils a Python package
```

---

### 4. `utils/theme.py` — Dual Theme Engine

**Purpose:** Centralized color management + theme-aware chart configuration

```python
# Theme detection via Streamlit session state
# Provides: get_theme(), get_colors(), get_plotly_layout(), get_chart_colors()
# The theme toggle in sidebar sets st.session_state["theme"]
# Charts and CSS adapt automatically based on current theme
```

**Key functions:**

| Function | Returns | Purpose |
|----------|---------|---------|
| `get_theme()` | `"dark"` or `"light"` | Current theme state |
| `toggle_theme()` | None | Switches theme in session state |
| `get_colors()` | `dict` | Full color palette for current theme |
| `get_plotly_template()` | `dict` | Plotly layout template (bg, text, grid colors) |
| `get_chart_colors()` | `list` | 10-color sequence for data series |
| `inject_custom_css()` | None | Injects theme-aware CSS into page |
| `render_sidebar()` | None | Logo + theme toggle + common sidebar elements |

---

### 5. `utils/data_loader.py` — Data Loading & Cleaning

**Purpose:** Cached loading of all 9 datasets with cleaning transformations

**Key design decisions:**

#### Column Renaming Map
```python
COLUMN_RENAMES = {
    "my angel": "Private",
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
}
```

#### License Type Columns (for files 1 & 8)
```python
LICENSE_TYPES = [
    "Private", "motorcycle", "Public bus", "transfer",
    "Temporary license", "Private bus", "Commercial",
    "Customs Private", "Tourist", "Diplomatic body",
    "Tourism bus", "Trips", "Motorbike", "Heavy Transport",
    "School bus", "Customs bus", "Suspended"
]
```

#### Data Cleaning Steps
1. Rename columns using the map above
2. Forward-fill merged Province values (Files 2, 3, 4, 5, 9)
3. Drop grand total / summary rows
4. Fill NaN numeric values with `0`
5. Remove unnamed columns OR rename to years (2022-2026) where applicable
6. Strip whitespace from string columns
7. Standardize Brand/Model casing

#### Loader Functions (all `@st.cache_data` decorated)

| Function | File(s) | Returns | Rows |
|----------|---------|---------|------|
| `load_ev_by_license()` | File 1 (CSV) | DataFrame | ~905 |
| `load_ev_january()` | File 8 (XLSX) | DataFrame | ~206 |
| `load_new_vehicles()` | File 2 (CSV) | DataFrame | ~11,282 |
| `load_new_private()` | File 3 (XLSX) | DataFrame | ~7,134 |
| `load_license_condition_gov()` | File 4 (XLSX) | DataFrame | ~30,267 |
| `load_vehicle_condition()` | File 5 (XLSX) | DataFrame | ~68,100 |
| `load_shape_engine()` | File 6 (XLSX) | DataFrame | ~1,255 |
| `load_private_by_gov()` | File 7 (XLSX) | DataFrame | ~2,690 |
| `load_used_vehicles()` | File 9 (XLSX) | DataFrame | ~11,282 |
| `load_all_summary()` | All files | dict of KPIs | Aggregated |

---

### 6. `utils/charts.py` — Reusable Chart Components

**Purpose:** Plotly chart builders that respect the current theme

| Function | Chart Type | Used On |
|----------|-----------|---------|
| `kpi_card(title, value, delta, icon)` | HTML metric card | All pages |
| `donut_chart(df, names, values, title)` | Plotly Pie (donut) | Fuel type, Country |
| `horizontal_bar(df, x, y, title, n)` | Plotly Bar (horizontal) | Top brands, rankings |
| `stacked_bar(df, x, y, color, title)` | Plotly Bar (stacked) | License types, governorates |
| `line_chart(df, x, y, title)` | Plotly Line | Year trends |
| `treemap_chart(df, path, values, title)` | Plotly Treemap | Country → Brand hierarchy |
| `heatmap_chart(df, x, y, z, title)` | Plotly Heatmap | Brand × Shape matrix |
| `histogram_chart(df, x, title)` | Plotly Histogram | Engine capacity distribution |
| `box_plot(df, x, y, title)` | Plotly Box | Engine size by brand |
| `data_table(df, title)` | st.dataframe | Searchable tables on all pages |

**All charts will:**
- Use `get_plotly_template()` for theme-aware backgrounds
- Use `get_chart_colors()` for consistent data series colors
- Include hover tooltips with formatted numbers
- Be responsive to container width

---

### 7. `app.py` — Home / Overview (Page 1)

**Layout:**

```
┌─────────────────────────────────────────────────────┐
│  [Logo]  AlAhram Gate Dashboard    [🌙/☀️ Toggle]   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐      │
│  │Total │ │ New  │ │ Used │ │ EVs  │ │Brands│      │
│  │131K+ │ │ 21K  │ │ 11K  │ │ 24K  │ │ 150+ │      │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘      │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  Fuel Type Donut    │  │  Top 10 Brands Bar     │ │
│  │  (all datasets)     │  │  (horizontal)          │ │
│  └─────────────────────┘  └────────────────────────┘ │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  Country Treemap    │  │  Year Trend 2022-2026  │ │
│  │  (manufacturing)    │  │  (line chart)          │ │
│  └─────────────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Data sources:** `load_all_summary()` aggregating from all 9 files

**Key logic:**
- 5 KPI metric cards using `st.columns(5)` + custom HTML cards
- Fuel type donut combining all datasets (deduplicated)
- Top 10 brands bar chart (aggregate Grand Total across files)
- Country treemap showing manufacturing origin hierarchy
- Year trend line chart from Used vehicles file (2022→2026 columns)

---

### 8. `pages/1_⚡_Electric_Vehicles.py` — Page 2

**Data sources:** `load_ev_by_license()` + `load_ev_january()`

**Sidebar filters:**
- Brand (multiselect)
- Country (multiselect)
- Vehicle Shape (multiselect)
- Fuel Sub-Type (multiselect: Electric, Plug-in Hybrid, Hybrid)

**Layout:**

```
┌─────────────────────────────────────────────────────┐
│  ⚡ Electric Vehicles Analysis                       │
├─────────────────────────────────────────────────────┤
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │Total   │ │Top     │ │Top     │ │Jan 2026│       │
│  │24,633  │ │BYD     │ │China   │ │Monthly │       │
│  └────────┘ └────────┘ └────────┘ └────────┘       │
│                                                      │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Top 15 EV Brands (Horizontal Bar)              │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  License Type       │  │  Country of Origin     │ │
│  │  Stacked Bar        │  │  Donut Chart           │ │
│  └─────────────────────┘  └────────────────────────┘ │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  Vehicle Shape      │  │  Fuel Sub-Type         │ │
│  │  Donut              │  │  Donut                 │ │
│  └─────────────────────┘  └────────────────────────┘ │
│                                                      │
│  📅 January 2026 Spotlight                           │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Top 10 brands table for Jan 2026 snapshot      │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  📋 Full Data Table (searchable, downloadable)       │
└─────────────────────────────────────────────────────┘
```

---

### 9. `pages/2_🆕_New_Vehicles.py` — Page 3

**Data sources:** `load_new_vehicles()` + `load_new_private()`

**Sidebar filters:**
- Province (multiselect)
- Traffic Unit (multiselect, dependent on Province)
- Brand (multiselect)
- Fuel Type (multiselect)
- Vehicle Shape (multiselect)

**Key feature:** Toggle between "All New Vehicles" and "Private Only" using `st.radio`

**Layout:**

```
┌─────────────────────────────────────────────────────┐
│  🆕 New Vehicles Market                              │
├─────────────────────────────────────────────────────┤
│  [All Vehicles ◉] [Private Only ○]                  │
│                                                      │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │Total   │ │Top     │ │Top     │ │Fuel    │       │
│  │Regs    │ │Province│ │Brand   │ │Split   │       │
│  └────────┘ └────────┘ └────────┘ └────────┘       │
│                                                      │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Top 15 Brands (Horizontal Bar)                 │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  Province Heatmap   │  │  Fuel Type Donut       │ │
│  │  (Top 15 Govs)      │  │                        │ │
│  └─────────────────────┘  └────────────────────────┘ │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  Traffic Unit Top10 │  │  Country of Origin     │ │
│  │  Bar Chart          │  │  Treemap               │ │
│  └─────────────────────┘  └────────────────────────┘ │
│                                                      │
│  📋 Full Data Table                                  │
└─────────────────────────────────────────────────────┘
```

---

### 10. `pages/3_🔧_Vehicle_Specs.py` — Page 4

**Data sources:** `load_shape_engine()` + `load_private_by_gov()`

**Sidebar filters:**
- Brand (multiselect)
- Body Shape (multiselect)
- Province (multiselect)
- Fuel Type (multiselect)

**Layout:**

```
┌─────────────────────────────────────────────────────┐
│  🔧 Vehicle Specifications                          │
├─────────────────────────────────────────────────────┤
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │Shapes  │ │Avg CC  │ │Top Gov │ │Top Type│       │
│  └────────┘ └────────┘ └────────┘ └────────┘       │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  Body Shape Donut   │  │  Engine CC Histogram   │ │
│  └─────────────────────┘  └────────────────────────┘ │
│                                                      │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Brand × Shape Heatmap                          │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  Governorate Prefs  │  │  Engine CC by Brand    │ │
│  │  Stacked Bar        │  │  Box Plot              │ │
│  └─────────────────────┘  └────────────────────────┘ │
│                                                      │
│  📋 Full Data Table                                  │
└─────────────────────────────────────────────────────┘
```

---

### 11. `pages/4_📊_Market_Distribution.py` — Page 5

**Data sources:** `load_license_condition_gov()` + `load_vehicle_condition()`

**Sidebar filters:**
- Province (multiselect)
- License Type (multiselect)
- Vehicle Condition (multiselect)
- Brand (multiselect)
- Country (multiselect)

> [!IMPORTANT]
> **Performance:** This page handles **98,367 rows**. Strategy:
> - Pre-aggregate data before charting
> - Use `@st.cache_data` with TTL
> - Limit default display to Top 20 per chart
> - Lazy-load the detailed data table

**Layout:**

```
┌─────────────────────────────────────────────────────┐
│  📊 Market Distribution & Conditions                 │
├─────────────────────────────────────────────────────┤
│  [By License Type ◉] [By Condition ○]               │
│                                                      │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │Total   │ │License │ │Govs    │ │Brands  │       │
│  │98K+    │ │Types   │ │Covered │ │Count   │       │
│  └────────┘ └────────┘ └────────┘ └────────┘       │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  License Type       │  │  Vehicle Condition     │ │
│  │  Distribution Pie   │  │  Distribution Bar      │ │
│  └─────────────────────┘  └────────────────────────┘ │
│                                                      │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Top 15 Governorates × License Type Stacked Bar │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  Top Brands by      │  │  Country × Condition   │ │
│  │  Condition (Grouped)│  │  Heatmap               │ │
│  └─────────────────────┘  └────────────────────────┘ │
│                                                      │
│  📋 Data Explorer (paginated)                        │
└─────────────────────────────────────────────────────┘
```

---

### 12. `pages/5_🔄_Used_Vehicles.py` — Page 6

**Data sources:** `load_used_vehicles()`

**Sidebar filters:**
- Province (multiselect)
- Traffic Unit (multiselect)
- Brand (multiselect)
- Manufacturing Year (slider: 2022-2026)
- Fuel Type (multiselect)

**Unique feature:** Year columns (2022, 2023, 2024, 2025, 2026) enable **trend analysis**

**Layout:**

```
┌─────────────────────────────────────────────────────┐
│  🔄 Used Vehicles Market                             │
├─────────────────────────────────────────────────────┤
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│  │Total   │ │Top     │ │Peak    │ │Top     │       │
│  │Used    │ │Brand   │ │Year    │ │Province│       │
│  └────────┘ └────────┘ └────────┘ └────────┘       │
│                                                      │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Year-over-Year Registration Trend (2022→2026)  │ │
│  │  Area/Line Chart                                │ │
│  └─────────────────────────────────────────────────┘ │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  Top 15 Used Brands │  │  Province Distribution │ │
│  │  Horizontal Bar     │  │  Horizontal Bar        │ │
│  └─────────────────────┘  └────────────────────────┘ │
│                                                      │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │  Fuel Type Donut    │  │  Country of Origin     │ │
│  │                     │  │  Treemap               │ │
│  └─────────────────────┘  └────────────────────────┘ │
│                                                      │
│  📋 Full Data Table                                  │
└─────────────────────────────────────────────────────┘
```

---

## 🔄 Theme Toggle Implementation

### How it works:

```
User clicks 🌙/☀️ toggle in sidebar
  → st.session_state["theme"] flips
  → st.rerun() triggers
  → inject_custom_css() applies new palette
  → All Plotly charts use get_plotly_template()
  → KPI cards use get_colors() for styling
```

### Custom CSS handles:
- Metric card backgrounds, borders, text colors
- Sidebar logo container with themed background
- Al-Ahram Red gradient top border (both themes)
- Gold accent underlines on section headers
- Hover effects on interactive elements
- Smooth transition animations between themes

---

## 🚀 Build Order (Step-by-Step)

| Step | Files | Description |
|------|-------|-------------|
| **1** | `requirements.txt`, `.streamlit/config.toml` | Project setup |
| **2** | `utils/__init__.py`, `utils/theme.py` | Theme engine with dual palettes |
| **3** | `utils/data_loader.py` | All 9 data loaders with caching + cleaning |
| **4** | `utils/charts.py` | Reusable Plotly chart components |
| **5** | `app.py` | Home page with KPIs + overview charts |
| **6** | `pages/1_⚡_Electric_Vehicles.py` | EV analysis page |
| **7** | `pages/2_🆕_New_Vehicles.py` | New vehicles market page |
| **8** | `pages/3_🔧_Vehicle_Specs.py` | Vehicle specifications page |
| **9** | `pages/4_📊_Market_Distribution.py` | Market distribution page |
| **10** | `pages/5_🔄_Used_Vehicles.py` | Used vehicles page |
| **11** | `README.md` | Documentation |

---

## ✅ Verification Plan

### Automated
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Manual Checklist
- [ ] All 6 pages load without errors
- [ ] Logo visible in sidebar on every page
- [ ] Theme toggle switches between dark/light correctly
- [ ] All charts render with correct color palette
- [ ] Sidebar filters work on every page
- [ ] Data tables are searchable and downloadable
- [ ] KPI numbers match raw dataset totals
- [ ] No NaN or broken values displayed
- [ ] Performance acceptable on largest page (98K rows)
