# 🏛️ AlAhram Gate Dashboard

An interactive data dashboard for **Al-Ahram Gate** (بوابة الأهرام), analyzing Egyptian vehicle registration statistics across 9 datasets covering electric vehicles, new vehicles, used vehicles, and market distribution.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

## 📊 Dashboard Pages

| Page | Description | Datasets |
|------|-------------|----------|
| 🏠 **Home Overview** | Aggregate KPIs, fuel type, top brands, country treemap, year trends | All 9 files |
| ⚡ **Electric Vehicles** | EV brands by license type, Jan 2026 spotlight | Files 1, 8 |
| 🆕 **New Vehicles** | New car registrations by location, brand, fuel type | Files 2, 3 |
| 🔧 **Vehicle Specs** | Body types, engine capacity, governorate preferences | Files 6, 7 |
| 📊 **Market Distribution** | License types, vehicle conditions, provincial breakdown | Files 4, 5 |
| 🔄 **Used Vehicles** | Year-over-year trends, used car market analysis | File 9 |

## 🎨 Features

- **Dual Theme**: Dark mode & Light mode toggle
- **Interactive Charts**: Plotly-powered with hover tooltips
- **Sidebar Filters**: Per-page filtering by brand, country, province, fuel type
- **Data Explorer**: Searchable tables with CSV download
- **Al-Ahram Branding**: Logo integration with Red & Gold color palette

## 🛠️ Tech Stack

- **Streamlit** — Web framework
- **Plotly** — Interactive charts
- **Pandas** — Data processing
- **OpenPyXL** — Excel file reading

## 📁 Project Structure

```
├── app.py                    ← Main entry point (Home page)
├── pages/                    ← Auto-discovered dashboard pages
├── utils/
│   ├── theme.py              ← Dual theme engine + CSS
│   ├── data_loader.py        ← Cached data loading + cleaning
│   └── charts.py             ← Reusable chart components
├── .streamlit/config.toml    ← Theme configuration
├── assets/logo.png           ← Al-Ahram logo
└── Dataset/                  ← 9 data files (CSV + XLSX)
```
