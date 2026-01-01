# 🏎️ F1 Data Engineering Project - Data Model Documentation

## Overview

This document describes the data model used in the F1 Data Engineering project, following the **Medallion Architecture** (Bronze → Silver → Gold) implemented in Azure Databricks.

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           F1 DATA PIPELINE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐               │
│  │   CSV Files  │ ───► │    BRONZE    │ ───► │    SILVER    │ ───► GOLD    │
│  │  (Raw Data)  │      │   (Raw Ingest)│      │  (Cleansed)  │      Tables  │
│  └──────────────┘      └──────────────┘      └──────────────┘               │
│                                                                              │
│  ├── circuits.csv      ├── circuits         ├── circuits        ┌─────────┐ │
│  ├── constructors.csv  ├── constructors     ├── constructors    │ Power   │ │
│  ├── drivers.csv       ├── drivers          ├── drivers         │   BI    │ │
│  ├── races.csv         ├── races            ├── races           │Dashboard│ │
│  ├── results.csv       ├── results          ├── results         └─────────┘ │
│  ├── qualifying.csv    ├── qualifying       ├── qualifying                  │
│  ├── lap_times.csv     ├── lap_times        ├── lap_times                   │
│  ├── pit_stops.csv     ├── pit_stops        ├── pit_stops                   │
│  ├── standings...      ├── standings...     ├── standings...                │
│  └── status.csv        └── status           └── status                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🥉 Bronze Layer (Raw Data)

The Bronze layer contains raw data ingested from CSV files with minimal transformation.

### Tables

| Table Name | Description | Row Count (Est.) |
|------------|-------------|-----------------|
| `f1_bronze.circuits` | Racing circuit information | ~80 |
| `f1_bronze.constructors` | F1 teams/constructors | ~210 |
| `f1_bronze.drivers` | Driver information | ~860 |
| `f1_bronze.races` | Race event details | ~1,100 |
| `f1_bronze.results` | Race results | ~27,000 |
| `f1_bronze.qualifying` | Qualifying results | ~10,000 |
| `f1_bronze.lap_times` | Individual lap times | ~500,000+ |
| `f1_bronze.pit_stops` | Pit stop records | ~10,000 |
| `f1_bronze.driver_standings` | Championship standings | ~30,000 |
| `f1_bronze.constructor_standings` | Constructor standings | ~14,000 |
| `f1_bronze.constructor_results` | Constructor race results | ~13,000 |
| `f1_bronze.seasons` | F1 seasons | ~75 |
| `f1_bronze.status` | Race finish statuses | ~140 |
| `f1_bronze.sprint_results` | Sprint race results | ~600 |

### Added Metadata Columns
- `ingestion_timestamp` - When the data was ingested
- `source_file` - Original source file name

---

## 🥈 Silver Layer (Cleansed Data)

The Silver layer contains cleaned and transformed data with proper data types and consistent naming.

### Key Transformations Applied

1. **Column Renaming**: CamelCase → snake_case
2. **Data Type Conversions**: Strings → Dates, Integers, Doubles
3. **Null Handling**: Proper NULL values instead of \N
4. **Derived Columns**: Full names, calculated fields
5. **Data Quality**: Validated relationships

### Tables & Schema

#### `f1_silver.circuits`
| Column | Type | Description |
|--------|------|-------------|
| circuit_id | INT | Primary Key |
| circuit_ref | STRING | Reference code |
| circuit_name | STRING | Full name |
| circuit_location | STRING | City/Location |
| circuit_country | STRING | Country |
| latitude | DOUBLE | GPS latitude |
| longitude | DOUBLE | GPS longitude |
| altitude_meters | INT | Altitude in meters |

#### `f1_silver.drivers`
| Column | Type | Description |
|--------|------|-------------|
| driver_id | INT | Primary Key |
| driver_ref | STRING | Reference code |
| driver_number | INT | Racing number |
| driver_code | STRING | 3-letter code (HAM, VER, etc.) |
| first_name | STRING | Forename |
| last_name | STRING | Surname |
| full_name | STRING | Combined first + last name |
| date_of_birth | DATE | DOB |
| driver_nationality | STRING | Nationality |

#### `f1_silver.constructors`
| Column | Type | Description |
|--------|------|-------------|
| constructor_id | INT | Primary Key |
| constructor_ref | STRING | Reference code |
| constructor_name | STRING | Team name |
| constructor_nationality | STRING | Team nationality |

#### `f1_silver.races`
| Column | Type | Description |
|--------|------|-------------|
| race_id | INT | Primary Key |
| race_year | INT | Season year |
| race_round | INT | Round number in season |
| circuit_id | INT | Foreign Key → circuits |
| race_name | STRING | Grand Prix name |
| race_date | DATE | Race date |
| race_time | STRING | Race start time |
| race_datetime | TIMESTAMP | Combined date + time |
| qualifying_date | DATE | Quali date |
| sprint_date | DATE | Sprint race date |

#### `f1_silver.results`
| Column | Type | Description |
|--------|------|-------------|
| result_id | INT | Primary Key |
| race_id | INT | FK → races |
| driver_id | INT | FK → drivers |
| constructor_id | INT | FK → constructors |
| grid_position | INT | Starting position |
| finish_position | INT | Final position |
| points_earned | DOUBLE | Points scored |
| laps_completed | INT | Laps finished |
| time_milliseconds | INT | Race time in ms |
| fastest_lap_rank | INT | FL rank in race |
| fastest_lap_speed_kph | DOUBLE | FL speed |
| status_id | INT | FK → status |
| **is_winner** | BOOLEAN | True if P1 |
| **is_podium** | BOOLEAN | True if P1-P3 |
| **is_points_finish** | BOOLEAN | True if scored points |
| **positions_gained** | INT | Grid - Finish position |

#### `f1_silver.status`
| Column | Type | Description |
|--------|------|-------------|
| status_id | INT | Primary Key |
| status_description | STRING | Full status text |
| status_category | STRING | Grouped category (Finished, Mechanical, Accident, etc.) |

---

## 🥇 Gold Layer (Analytics Ready)

The Gold layer contains aggregated, denormalized tables optimized for analytics and Power BI.

### Tables

#### `f1_gold.fact_race_results` (Primary Fact Table)
Fully denormalized race results with all dimension attributes.

| Column | Type | Description |
|--------|------|-------------|
| result_id | INT | Primary Key |
| race_id | INT | Race identifier |
| driver_id | INT | Driver identifier |
| constructor_id | INT | Team identifier |
| grid_position | INT | Starting grid |
| finish_position | INT | Final position |
| points_earned | DOUBLE | Points scored |
| is_winner | BOOLEAN | Won the race |
| is_podium | BOOLEAN | Finished P1-P3 |
| positions_gained | INT | Positions gained/lost |
| race_year | INT | Season year |
| race_name | STRING | Grand Prix name |
| race_date | DATE | Race date |
| driver_name | STRING | Full driver name |
| driver_code | STRING | 3-letter code |
| driver_nationality | STRING | Driver nationality |
| constructor_name | STRING | Team name |
| circuit_name | STRING | Circuit name |
| circuit_country | STRING | Circuit country |
| status_description | STRING | Finish status |
| status_category | STRING | Status category |

**Partitioned by**: `race_year`

---

#### `f1_gold.dim_driver_career` (Driver Statistics)
Career aggregations for each driver.

| Column | Type | Description |
|--------|------|-------------|
| driver_id | INT | Primary Key |
| driver_name | STRING | Full name |
| driver_nationality | STRING | Nationality |
| total_races | INT | Career race starts |
| total_wins | INT | Career wins |
| total_podiums | INT | Career podiums |
| total_pole_positions | INT | Career poles |
| total_fastest_laps | INT | Career fastest laps |
| total_career_points | DOUBLE | Lifetime points |
| avg_finish_position | DOUBLE | Average finish |
| avg_grid_position | DOUBLE | Average grid |
| debut_year | INT | First F1 season |
| last_season | INT | Most recent season |
| seasons_competed | INT | Total seasons |
| win_percentage | DOUBLE | Win % |
| podium_percentage | DOUBLE | Podium % |

---

#### `f1_gold.dim_constructor_performance` (Team Statistics)
Career aggregations for each constructor/team.

| Column | Type | Description |
|--------|------|-------------|
| constructor_id | INT | Primary Key |
| constructor_name | STRING | Team name |
| total_race_entries | INT | Total entries |
| total_wins | INT | Race wins |
| total_podiums | INT | Podium finishes |
| total_pole_positions | INT | Poles |
| total_points | DOUBLE | All-time points |
| avg_finish_position | DOUBLE | Average finish |
| total_drivers | INT | Drivers used |
| win_rate | DOUBLE | Win percentage |
| podium_rate | DOUBLE | Podium percentage |

---

#### `f1_gold.agg_driver_championships`
Season-end driver championship standings.

| Column | Type | Description |
|--------|------|-------------|
| season | INT | Year |
| driver_id | INT | Driver ID |
| driver_name | STRING | Full name |
| championship_points | DOUBLE | Final points |
| championship_position | INT | Final position |
| total_wins | INT | Wins in season |
| is_champion | BOOLEAN | Won championship |

---

#### `f1_gold.agg_constructor_championships`
Season-end constructor championship standings.

---

#### `f1_gold.agg_circuit_statistics`
Performance metrics per circuit.

| Column | Type | Description |
|--------|------|-------------|
| circuit_name | STRING | Circuit name |
| circuit_country | STRING | Country |
| total_races_hosted | INT | Races held |
| first_race_year | INT | First F1 race |
| dnf_rate | DOUBLE | DNF percentage |
| avg_positions_gained | DOUBLE | Typical position changes |

---

#### `f1_gold.agg_driver_season_performance`
Driver stats by season for year-over-year analysis.

---

#### `f1_gold.agg_constructor_season_performance`
Constructor stats by season.

---

## 🔗 Entity Relationship Diagram

```
                           ┌─────────────┐
                           │   SEASONS   │
                           │  (year)     │
                           └──────┬──────┘
                                  │
                                  ▼
┌─────────────┐           ┌─────────────┐           ┌─────────────┐
│  CIRCUITS   │◄──────────│    RACES    │───────────►│   STATUS    │
│ (circuit_id)│           │  (race_id)  │           │ (status_id) │
└─────────────┘           └──────┬──────┘           └─────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────┐           ┌─────────────┐           ┌─────────────┐
│  QUALIFYING │           │   RESULTS   │           │  PIT_STOPS  │
│(qualify_id) │           │(result_id)  │           │             │
└──────┬──────┘           └──────┬──────┘           └──────┬──────┘
       │                         │                         │
       │              ┌──────────┴──────────┐             │
       │              │                     │             │
       ▼              ▼                     ▼             ▼
┌─────────────┐ ┌─────────────┐     ┌─────────────┐
│   DRIVERS   │ │CONSTRUCTORS │     │  LAP_TIMES  │
│ (driver_id) │ │(constructor_│     │             │
└─────────────┘ │    id)      │     └─────────────┘
                └─────────────┘
```

---

## 📈 Key Metrics & KPIs

### Driver KPIs
- 🏆 Total Wins
- 🥇 Win Percentage
- 🥉 Podium Rate
- ⏱️ Average Finish Position
- 🔄 Positions Gained/Lost
- 🎯 Points per Race

### Constructor KPIs
- 🏭 Total Team Wins
- 📊 Championship Points
- 👥 Driver Count
- ⚡ Pole Position Rate

### Race KPIs
- 🚗 DNF Rate
- 🔄 Position Changes
- ⏱️ Fastest Lap
- 🛑 Pit Stop Duration

---

## 🔄 Data Refresh Strategy

| Layer | Refresh Frequency | Method |
|-------|-------------------|--------|
| Bronze | Weekly (or as new data arrives) | Full refresh |
| Silver | After Bronze refresh | Incremental/Full |
| Gold | After Silver refresh | Full rebuild |

---

## ✅ Data Quality Checks

1. **Primary Key Uniqueness**: All IDs are unique
2. **Foreign Key Validity**: All FKs reference valid PKs
3. **Null Handling**: Critical fields are not null
4. **Date Validation**: All dates are valid
5. **Range Checks**: Points, positions within expected ranges
