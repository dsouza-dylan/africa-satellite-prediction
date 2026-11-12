# Raw Data

Raw data is not committed to this repository because of license restrictions on redistribution. Follow the instructions below to recreate this folder locally. After downloading, the expected structure is:

```
data/raw/
├── gdl_indicators/
│   ├── Area Database Data v441.csv
│   ├── Area Database Labels v441.csv
│   ├── Education and Work Data v2.1.csv
│   ├── Education and Work Labels v2.1.csv
│   ├── Health Data v2.1.csv
│   ├── Health Labels v2.1.csv
│   ├── Subnational HDI Data v10.2.csv
│   ├── Subnational HDI Labels v10.2.csv
│   ├── Wealth Data v2.1.csv
│   └── Wealth Labels v2.1.csv
├── mosaiks/
│   ├── GDL_ADM1_polygon_X_creation.csv
│   └── GDL_ADM1_polygon_X_creation_GHS_POP.csv
└── shapefiles/
    ├── shdi2022_World_large.shp
    ├── shdi2022_World_large.shx
    ├── shdi2022_World_large.dbf
    └── shdi2022_World_large.prj
```

---

## 1. GDL Subnational Indicators

**Source:** [Global Data Lab](https://globaldatalab.org/mygdl/downloads/), which requires a free account.

**Version pins used in this project:**
| File | Version | Purpose |
|------|---------|---------|
| Area Database Data | v441 | Urban population share |
| Education and Work Data | v2.1 | Expected years of schooling (girls, boys) |
| Health Data | v2.1 | Stunting, under-five mortality, DTP3 coverage |
| Subnational HDI Data | v10.2 | SHDI, regional population |
| Wealth Data | v2.1 | International Wealth Index, poverty headcount |

**Download steps:**
1. Create a free account to access [Global Data Lab](https://globaldatalab.org/mygdl/downloads/).
2. Download the five "Data" CSVs and (optionally) their accompanying "Labels" (variable dictionary) files at the version numbers listed above.
3. Place all files in `data/raw/gdl_indicators/` using the exact filenames shown above.

**Citation:** 
Smits, J., & Permanyer, I. (2019). *The Subnational Human Development Database*. Scientific Data, 6, 190038. https://doi.org/10.1038/sdata.2019.38

---

## 2. MOSAIKS Satellite Features

**Source:** [MOSAIKS precomputed dataset](https://www.mosaiks.org/precomputed), which requires a free Redivis account.

**Version used:** 
MOSAIKS features pre-aggregated to Global Data Lab v6.1 ADM1 boundaries.

**Files required:**
- `GDL_ADM1_polygon_X_creation.csv` (area-weighted)
- `GDL_ADM1_polygon_X_creation_GHS_POP.csv` (population-weighted)

**Download steps:**
1. Create a free account to access [MOSAIKS precomputed dataset](https://www.mosaiks.org/precomputed).
2. Locate the MOSAIKS precomputed ADM1 features dataset and download both the area-weighted and population-weighted CSVs.
3. Place both files in `data/raw/mosaiks/`.

**Note on filename identification:** 
The `_GHS_POP` suffix indicates population-weighted; the file without a suffix is area-weighted. Feature values differ meaningfully between the two files.

**Citation:** 
Rolf, E., Proctor, J., Carleton, T., et al. (2021). *A generalizable and accessible approach to machine learning with global satellite imagery*. Nature Communications, 12, 4392. https://doi.org/10.1038/s41467-021-24638-z

---

## 3. GDL v6.1 Shapefiles

**Source:** [Global Data Lab shapefile repository](https://globaldatalab.org/shdi/shapefiles/), which is accessible through the GDL account.

**Files required:**
- `shdi2022_World_large.shp` (geometry)
- `shdi2022_World_large.shx` (index)
- `shdi2022_World_large.dbf` (attributes)
- `shdi2022_World_large.prj` (projection)

**Download steps:**
1. Download the v6.1 shapefile bundle (`shdi2022_World_large`).
2. Place all four files (`.shp`, `.shx`, `.dbf`, `.prj`) in `data/raw/shapefiles/`.

---

## Reproducibility notes
- All files were downloaded in October 2026 at the version numbers pinned above.
- GDL updates its data periodically: later versions should produce qualitatively similar results but may differ in exact R² values.
- MOSAIKS pre-aggregated files are a one-off release and are not expected to change.
- No modifications are made to the raw files, and all processing takes place downstream.
