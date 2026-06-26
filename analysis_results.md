# 🏛️ AlAhram Gate Dashboard — Project Analysis

## Project Overview

This project is a **data-driven dashboard** for **Al-Ahram Gate** (بوابة الأهرام), the digital portal of Egypt's most prominent newspaper. The repository currently contains **raw datasets** about vehicle registration statistics in Egypt — no application code has been built yet.

---

## 📁 Project Structure

```
AlAhram-Gate-Dashboard/
├── .git/
├── assets/
│   └── logo.png                          ← Al-Ahram newspaper logo (58 KB)
└── Dataset/
    └── DATA AFTER FUEL TYPE/
        ├── 📄 Electric vehicles by license type (.csv)
        ├── 📄 Zero/new vehicles by location (.csv)
        ├── 📊 Zero private car brands & models (.xlsx)
        ├── 📊 Brands by license, condition & governorate (.xlsx)
        ├── 📊 Brands by vehicle condition (.xlsx)
        ├── 📊 Private zero cars by shape & engine capacity (.xlsx)
        ├── 📊 Private zero car brands by governorate (.xlsx)
        ├── 📊 Electric vehicles by license (Jan 2026) (.xlsx)
        └── 📊 Used vehicle brands & models (.xlsx)
```

> [!NOTE]
> The `fuel_after_map` prefix on all files indicates a **data enrichment pipeline** has already been applied, adding `Country`, `Shape`, and `Fuel_Type` columns to the raw registration data.

---

## 📊 Dataset Deep Dive

### File 1: Electric Vehicle Brands by License Type
| Attribute | Value |
|-----------|-------|
| **Format** | CSV (53 KB) |
| **Rows** | ~905 data rows + 1 grand total |
| **Columns** | 23 |
| **Total Vehicles** | **24,633** |
| **Focus** | Electric & alternative-fuel vehicles |
| **Geographic** | National aggregate (no province breakdown) |

#### Column Breakdown (23 columns)

| Column | Type | Description |
|--------|------|-------------|
| `Brand` | String | Vehicle manufacturer |
| `Model` | String | Vehicle model name |
| `my angel` | Float | Private license count (ملاكي) — **86.6% of total** |
| `motorcycle` | Float | Motorcycle license count |
| `Public bus` | Float | Public bus license count |
| `transfer` | Float | Transfer license count |
| `Temporary license` | Float | Temporary license count |
| `Private bus` | Float | Private bus license count |
| `brick` | Float | Unknown license type |
| `Malaki customs` | Float | Royal customs license count |
| `Tourist fare` | Float | Tourist license count |
| `Diplomatic body` | Float | Diplomatic license count |
| `Tourism bus` | Float | Tourism bus license count |
| `Trips` | Float | Trip license count |
| `Motorbike fare` | Float | Motorbike fare count |
| `Heavy stomach` | Float | Heavy transport (نقل ثقيل) |
| `School bus` | Float | School bus license count |
| `Customs bus` | Float | Customs bus count |
| `Turn off` | Float | Unknown license type |
| `Grand Total` | Integer | Total across all license types |
| `Country` | String | Country of origin |
| `Shape` | String | Vehicle body type |
| `Fuel_Type` | String | Fuel type |

> [!WARNING]
> Column names are **machine-translated from Arabic** with some inaccurate translations:
> - `my angel` → should be **"Private"** (ملاكي)
> - `Heavy stomach` → should be **"Heavy Transport"** (نقل ثقيل)
> - `brick` → unclear original Arabic term

#### Top Brands (Electric Vehicles)

```
BYD           ██████████████████████████████  ~3,800+
Volkswagen    ████████████████████████████    ~3,500+
Mercedes-Benz ████████████████                ~2,000+
BMW           ███████████                     ~1,400+
Nissan        ████████                        ~990+
Tesla         █████                           ~670+
ROX           █████                           ~572
XPeng         ████                            ~552
```

#### License Type Distribution

```
Private (ملاكي)    ██████████████████████████████  21,325 (86.6%)
Motorcycle         ██                                884
Public Bus         ██                                761
Transfer           █                                 639
Temporary          █                                 439
Other types        ░                                 585
```

#### Key Dimensions
- **Countries:** 20+ (China, Germany, Japan, USA, South Korea, UK, Sweden, France, Italy, India, Egypt, etc.)
- **Shapes:** SUV, Sedan, Hatchback, Bus, Pickup, Van, Wagon, Motorcycle, Minivan, Coupe, Convertible, Truck
- **Fuel Types:** Electric (~85%), Petrol, Plug-in Hybrid, Diesel, Hybrid

---

### File 2: Zero (New) Vehicle Brands by Location
| Attribute | Value |
|-----------|-------|
| **Format** | CSV (889 KB) |
| **Rows** | ~11,282 data rows |
| **Columns** | 14 |
| **Focus** | ALL brand-new vehicles (not just electric) |
| **Geographic** | By province & traffic unit |

#### Column Breakdown (14 columns)

| Column | Type | Description |
|--------|------|-------------|
| `M` | Float | Row index |
| `Issuance province` | String | Province where license was issued |
| `port` | String | Traffic unit / registration office |
| `Brand` | String | Vehicle manufacturer |
| `Model` | String | Vehicle model name |
| `Year of manufacture` | Float | Manufacturing year (mostly empty) |
| `Unnamed: 6-9` | Float | Sparse numeric breakdowns (headers lost) |
| `General total` | Float | Total vehicle count |
| `Country` | String | Country of origin |
| `Shape` | String | Vehicle body type |
| `Fuel_Type` | String | Fuel type |

> [!IMPORTANT]
> This dataset uses **merged-cell-style** representation — province values only appear on the first row of each group, with blanks for subsequent rows. This will need forward-filling during data processing.

#### Key Characteristics
- **Dominant fuel type:** Petrol (unlike File 1 which is Electric-dominant)
- **Top brands:** MG, Nissan, Mercedes-Benz, Volkswagen, Hyundai, Chery, Toyota, BYD, Kia, Chevrolet, BMW
- **Geographic coverage:** All Egyptian governorates (Cairo, Alexandria, Giza, etc.)
- **4 unnamed columns** (6-9) likely represent year-based or category-based breakdowns

---

### Additional Excel Files (7 files, not fully parsed)

| File | Size | Likely Content |
|------|------|----------------|
| Zero private car brands & models | 292 KB | Private ("ملاكي") new car registrations |
| Brands by license, condition & governorate | 1.2 MB | Cross-tabulation by 3 dimensions |
| Brands by vehicle condition | 2.8 MB | Largest file — condition-based breakdown |
| Private zero by shape & engine capacity | 44 KB | Body type × engine size analysis |
| Private zero brands by governorate | 101 KB | Geographic distribution of new private cars |
| Electric by license (Jan 2026) | 13 KB | Monthly snapshot — January 2026 |
| Used vehicle brands & models | 472 KB | Second-hand vehicle registrations |

---

## 🖼️ Logo

The [logo.png](file:///d:/Projects/AlAhram-Gate-Dashboard/assets/logo.png) is the iconic **Al-Ahram (الأهرام)** newspaper branding featuring:
- Bold Arabic calligraphy of "الأهرام" (The Pyramids)
- Two red pyramid shapes with brick pattern in the background
- Clean white background — ready for dashboard integration

---

## 📈 Dataset Comparison Matrix

| Dimension | File 1 (Electric × License) | File 2 (New × Location) |
|-----------|------------------------------|--------------------------|
| **Rows** | 905 | 11,282 |
| **Size** | 53 KB | 889 KB |
| **Columns** | 23 | 14 |
| **Primary Key** | Brand + Model | Province + Unit + Brand + Model |
| **Geographic?** | ❌ National aggregate | ✅ By province & traffic unit |
| **License type?** | ✅ 17 license types | ❌ |
| **Vehicle focus** | Electric/alt-fuel only | All new vehicles |
| **Dominant fuel** | Electric | Petrol |
| **Shared columns** | `Brand`, `Model`, `Country`, `Shape`, `Fuel_Type` |

---

## 🔍 Data Quality Observations

1. **Machine-translated column names** — Several columns have inaccurate English names that should be corrected in the dashboard
2. **Sparse data** — Many license-type columns in File 1 are mostly empty (only Private has consistent data)
3. **Merged-cell artifacts** — File 2's province column needs forward-filling
4. **4 unnamed columns** in File 2 — Headers were lost during export
5. **Duplicate/variant model names** — e.g., "Leopard" vs "Leopard 3" may need normalization
6. **Grand Total row** in File 1 — Should be excluded from visualizations

---

## 🚀 Dashboard Potential

This data is rich enough to power a compelling dashboard with:

- **Brand market share** pie/donut charts
- **Country of origin** analysis (geographic treemap)
- **Vehicle shape** distribution
- **Fuel type** breakdown (Electric vs Petrol vs Hybrid)
- **License type** analysis (File 1)
- **Geographic heatmap** of registrations by governorate (File 2)
- **Top models** ranked bar charts
- **EV adoption trends** using the Jan 2026 monthly file
- **New vs Used** vehicle comparisons
