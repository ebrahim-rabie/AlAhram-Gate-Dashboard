# 🏛️ AlAhram Gate Dashboard — Coverage Plan

## Answer: **6 Dashboard Pages** Cover All 9 Datasets

To fully represent all your data without redundancy, you need **6 dashboard pages** — a Home overview plus 5 specialized pages. Here's the complete mapping:

---

## 📋 Complete Dataset Inventory

| # | File | Rows | Columns | Key Dimensions |
|---|------|------|---------|----------------|
| 1 | EV brands by license type (CSV) | 905 | 23 | Brand, Model, 17 license types |
| 2 | New vehicles by location (CSV) | 11,282 | 14 | Province, Traffic Unit, Brand, Model, Years |
| 3 | New private (ملاكي) vehicles (XLSX) | 7,134 | 14 | Province, Traffic Unit, Brand, Model |
| 4 | Brands by license type & condition × governorate (XLSX) | 30,267 | 13 | Province, License Type, Brand, Model |
| 5 | Brands by vehicle condition (XLSX) | 68,100 | 13 | Province, Traffic Unit, Vehicle Condition, Brand |
| 6 | Private zero by shape & engine capacity (XLSX) | 1,255 | 7 | Brand, Model, Body Shape, Engine CC |
| 7 | Private zero brands by governorate (XLSX) | 2,690 | 8 | Province, Brand, Model |
| 8 | EV by license type — Jan 2026 (XLSX) | 206 | 15 | Brand, Model, License Types (monthly) |
| 9 | Used vehicles by location (XLSX) | 11,282 | 14 | Province, Traffic Unit, Brand, Year (2022-2026) |

> **Total: ~131,000+ rows across 9 files**

---

## 🗂️ File → Dashboard Mapping

```
              Page 1   Page 2   Page 3   Page 4   Page 5   Page 6
              Home     EV       New      Specs    Market   Used
File 1 (EV)    ✦        ●
File 2 (New)   ✦                 ●
File 3 (Priv)  ✦                 ●
File 4 (Lic)   ✦                                   ●
File 5 (Cond)  ✦                                   ●
File 6 (Spec)  ✦                          ●
File 7 (Gov)   ✦                          ●
File 8 (EV26)  ✦        ●
File 9 (Used)  ✦                                            ●

● = Primary data source    ✦ = Aggregated KPIs
```

---

## 📄 Page 1: Home / Overview
> *Aggregated KPIs from ALL 9 datasets*

### Data Sources
All files contribute summary metrics

### Key Visualizations
| Widget | Description |
|--------|-------------|
| 🔢 **KPI Cards** | Total vehicles, Total new, Total used, Total EVs, Countries, Brands |
| 🍩 **Fuel Type Donut** | Electric vs Petrol vs Hybrid vs Diesel (all datasets) |
| 🌍 **Country Treemap** | Top manufacturing countries across all vehicles |
| 📊 **Top 10 Brands Bar** | Overall brand ranking |
| 🗺️ **Egypt Governorate Map** | Registration density heatmap |
| 📈 **Year Trend Line** | 2022→2026 registration trend (from Used vehicles data) |

---

## 📄 Page 2: Electric Vehicles (EV) Dashboard
> *Focus: EV adoption, brands, and license distribution*

### Data Sources
- **File 1:** EV brands by license type — all time (905 rows)
- **File 8:** EV brands by license type — January 2026 (206 rows)

### Key Visualizations
| Widget | Description |
|--------|-------------|
| 🔢 **KPI Cards** | Total EVs (24,633), EV brands count, Top EV brand, Monthly new EVs |
| 🏆 **Top EV Brands** | Horizontal bar chart (BYD, VW, Mercedes, BMW, Tesla...) |
| 📊 **License Type Breakdown** | Stacked bar — Private vs Bus vs Motorcycle etc. |
| 🌍 **Country of Origin** | Donut chart (China vs Germany vs Japan vs USA) |
| 🚗 **Vehicle Shape** | SUV vs Sedan vs Hatchback distribution |
| ⚡ **Fuel Sub-Type** | Electric vs Plug-in Hybrid vs Hybrid |
| 📅 **Jan 2026 Spotlight** | Monthly snapshot comparison table |
| 📋 **Detailed Table** | Searchable/sortable brand-model table |

---

## 📄 Page 3: New (Zero) Vehicles Market
> *Focus: Brand-new vehicle registrations across Egypt*

### Data Sources
- **File 2:** All new vehicles by location (11,282 rows)
- **File 3:** New private (ملاكي) vehicles (7,134 rows)

### Key Visualizations
| Widget | Description |
|--------|-------------|
| 🔢 **KPI Cards** | Total new registrations, Top province, Top brand, Private vs all |
| 🗺️ **Geographic Heatmap** | Registrations by governorate |
| 🏆 **Top Brands** | Bar chart — MG, Nissan, Hyundai, Chery, Toyota... |
| 📍 **Traffic Unit Ranking** | Top registration offices (New Cairo, Nasr City...) |
| 🌍 **Country of Origin** | Manufacturing country breakdown |
| ⚡ **Fuel Type Mix** | Petrol vs Electric vs Diesel for new cars |
| 🚗 **Body Type** | Sedan vs SUV vs Hatchback |
| 📊 **Private vs All** | Comparison of private-only vs all license types |

---

## 📄 Page 4: Vehicle Specifications
> *Focus: Body types, engine capacities, and geographic preferences*

### Data Sources
- **File 6:** Private zero by shape & engine capacity (1,255 rows)
- **File 7:** Private zero brands by governorate (2,690 rows)

### Key Visualizations
| Widget | Description |
|--------|-------------|
| 🔢 **KPI Cards** | Unique shapes, Avg engine CC, Top governorate, Top body type |
| 🚗 **Body Shape Distribution** | Limousine vs SUV vs Hatchback (pie chart) |
| ⛽ **Engine Capacity Histogram** | Distribution of engine sizes (cc) |
| 📊 **Brand × Shape Matrix** | Heatmap of brands vs body types |
| 🗺️ **Governorate Preferences** | Which brands dominate in which provinces |
| 📈 **Engine Size by Brand** | Scatter/box plot of CC range per brand |
| 📋 **Detailed Table** | Full searchable data with filters |

---

## 📄 Page 5: Market Distribution & Conditions
> *Focus: License types, vehicle conditions, and governorate distribution*

### Data Sources
- **File 4:** Brands by license type & condition × governorate (30,267 rows)
- **File 5:** Brands by vehicle condition (68,100 rows)

### Key Visualizations
| Widget | Description |
|--------|-------------|
| 🔢 **KPI Cards** | Total vehicles, Governorates covered, License types, Conditions |
| 📊 **License Type Breakdown** | Malaki vs Transfer vs Bus etc. |
| 🔄 **Vehicle Condition** | New vs Used vs Condition distribution |
| 🗺️ **Governorate × License** | Stacked bars by province |
| 🏆 **Top Brands by Condition** | Which brands dominate new vs used |
| 📍 **Traffic Unit Analysis** | Registration patterns by office |
| 🌍 **Country × Condition** | Manufacturing origin by vehicle condition |
| 📋 **Cross-Tab Explorer** | Interactive pivot table |

> [!NOTE]
> This is the **largest data page** (98,367 combined rows). Consider server-side pagination or data aggregation for performance.

---

## 📄 Page 6: Used Vehicles Market
> *Focus: Second-hand vehicle trends and year-over-year analysis*

### Data Sources
- **File 9:** Used vehicles by location (11,282 rows)

### Key Visualizations
| Widget | Description |
|--------|-------------|
| 🔢 **KPI Cards** | Total used vehicles, Top used brand, Peak year, Top province |
| 📈 **Year-over-Year Trend** | Line chart 2022→2026 registration volumes |
| 🏆 **Top Used Brands** | MG, Nissan, Mercedes, Hyundai rankings |
| 🗺️ **Geographic Distribution** | Used car hotspots by governorate |
| 📍 **Traffic Unit Ranking** | Where used cars get registered most |
| 🌍 **Country of Origin** | Manufacturing countries for used market |
| ⚡ **Fuel Type** | Petrol vs Electric vs Diesel in used market |
| 📊 **New vs Used Comparison** | Side-by-side with Page 3 data |

---

## 🏗️ Summary

| Page | Name | Files Used | Total Rows | Focus |
|------|------|------------|------------|-------|
| 1 | **Home / Overview** | All 9 | ~131K | Aggregate KPIs |
| 2 | **Electric Vehicles** | 1, 8 | ~1,111 | EV brands & license types |
| 3 | **New Vehicles Market** | 2, 3 | ~18,416 | New car registrations by location |
| 4 | **Vehicle Specifications** | 6, 7 | ~3,945 | Body types & engine capacity |
| 5 | **Market Distribution** | 4, 5 | ~98,367 | License types & vehicle conditions |
| 6 | **Used Vehicles** | 9 | ~11,282 | Second-hand market & trends |

> [!IMPORTANT]
> ### Open Questions
> 1. **Language preference?** — Should the dashboard be in **Arabic**, **English**, or **bilingual**?
> 2. **Tech preference?** — Pure HTML/CSS/JS with Chart.js, or a framework like React/Next.js?
> 3. **Any priority pages?** — Should I build all 6 at once or start with specific pages?
> 4. **Interactivity level?** — Read-only visualizations or interactive filters/drill-downs?
> 5. **The "Unnamed" columns** (6-9) in files 2-5 — do you know what they represent? File 9 reveals they might be **year columns (2022-2026)**.
