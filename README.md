# 🏎️ F1 Data Engineering Project

<div align="center">

![Azure Databricks](https://img.shields.io/badge/Azure%20Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**A comprehensive end-to-end data engineering project processing Formula 1 racing data using Azure Databricks with Medallion Architecture**


</div>

---

## Project Overview

This project demonstrates a **production-ready data engineering pipeline** that:

- **Ingests** raw F1 CSV data from [Open databay](https://www.opendatabay.com/data/dataset/c27b4a97-d2e1-4c24-9093-237be4825085)
- **Transforms** data through Bronze → Silver → Gold layers
- **Visualizes** insights in interactive Power BI dashboards
- **Implements** best practices with Delta Lake & Unity Catalog


## Architecture
<div align="center">

![F1 Analytics Dashboard](/Architecture.png)

</div>


### Data Flow

| Layer | Purpose | Transformations | Tables |
|-------|---------|-----------------|--------|
| **Bronze** | Raw storage | Metadata only | 14 |
| **Silver** | Cleansed data | Type conversion, derived columns | 11 |
| **Gold** | Analytics ready | Aggregations, denormalization | 8 |

### DataBricks Job
<div align="center">

![F1 Analytics Dashboard](/job.png)

</div>

## Project Structure

```
F1_Project/
│
├── Data_source/                          # Raw source data (CSV)
│   ├── circuits.csv
│   ├── constructors.csv
│   ├── drivers.csv
│   ├── races.csv
│   ├── results.csv
│   ├── qualifying.csv
│   ├── lap_times.csv
│   ├── pit_stops.csv
│   ├── driver_standings.csv
│   ├── constructor_standings.csv
│   ├── constructor_results.csv
│   ├── seasons.csv
│   ├── status.csv
│   └── sprint_results.csv
│
├── notebooks/                            # Databricks notebooks
│   ├── 01_bronze_layer_ingestion.ipynb     # Bronze ETL pipeline
│   ├── 02_silver_layer_transformation.ipynb # Silver ETL pipeline
│   ├── 03_gold_layer_aggregations.ipynb    # Gold ETL pipeline
│   └── Create external locations.ipynb     # Storage setup
│
├── Chart/                                # Dashboard screenshots
│   └── F1_Dashboard.png                    # Power BI screenshot
│
├── docs/                                 # Documentation
│   ├── DATA_MODEL.md                       # Schema documentation
│   ├── POWERBI_INTEGRATION.md              # BI setup guide
│   └── POWERBI_DASHBOARD_DESIGN.md         # Dashboard specifications
│
├── F1_DashBoard.pbix                        # Power BI report file
├── SKILL.md                                 # Skills showcase
└── README.md                                # This file
```

## 📊 Power BI Dashboard

### Dashboard Preview

<div align="center">

![F1 Analytics Dashboard](Chart/F1_Dashboard.png)

</div>

---

</div>
