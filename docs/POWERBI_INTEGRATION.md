# 🏎️ F1 Data Project - Power BI Integration Guide

## Overview

This guide explains how to connect Power BI to your Azure Databricks F1 data and build interactive dashboards.

---

## 📊 Connection Methods

### Method 1: Azure Databricks Connector (Recommended)

1. **In Power BI Desktop:**
   - Get Data → Azure → Azure Databricks
   
2. **Enter Connection Details:**
   - Server Hostname: `<your-workspace>.azuredatabricks.net`
   - HTTP Path: `/sql/1.0/warehouses/<your-warehouse-id>` or `/sql/protocolv1/o/<org-id>/<cluster-id>`
   
3. **Authentication:**
   - Use Azure Active Directory or Personal Access Token (PAT)

4. **Select Tables:**
   - Navigate to `f1_gold` database
   - Select the Gold layer tables for reporting

### Method 2: Partner Connect (Databricks SQL)

1. In Databricks workspace, go to **Partner Connect**
2. Select **Power BI**
3. Follow the guided setup

### Method 3: Direct Query vs Import

| Mode | Use Case | Pros | Cons |
|------|----------|------|------|
| **Import** | Static reports, scheduled refresh | Fast queries, offline access | Data freshness depends on refresh |
| **DirectQuery** | Real-time dashboards | Always current data | Slower queries, requires connection |

**Recommendation:** Use **Import** mode for most F1 analytics dashboards.

---

## 📋 Recommended Gold Tables for Power BI

### Primary Tables to Import

| Table | Use Case | Refresh |
|-------|----------|---------|
| `f1_gold.fact_race_results` | Primary fact table for all race analysis | Daily/Weekly |
| `f1_gold.dim_driver_career` | Driver career statistics | Weekly |
| `f1_gold.dim_constructor_performance` | Team performance metrics | Weekly |
| `f1_gold.agg_driver_championships` | Championship history | Weekly |
| `f1_gold.agg_constructor_championships` | Constructor championship history | Weekly |
| `f1_gold.agg_circuit_statistics` | Circuit analytics | Weekly |
| `f1_gold.agg_driver_season_performance` | YoY driver analysis | Weekly |

---

## 🔗 Power BI Data Model

### Recommended Relationships

```
                    ┌─────────────────────┐
                    │  fact_race_results  │
                    │   (Central Fact)    │
                    └─────────┬───────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌────────────────┐    ┌────────────────┐
│dim_driver_   │    │dim_constructor_│    │agg_circuit_    │
│   career     │    │  performance   │    │  statistics    │
└──────────────┘    └────────────────┘    └────────────────┘
```

### Creating Relationships in Power BI

1. **fact_race_results → dim_driver_career**
   - Join: `driver_id` (Many to One)
   - Cross filter: Both

2. **fact_race_results → dim_constructor_performance**
   - Join: `constructor_id` (Many to One)
   - Cross filter: Both

3. **fact_race_results → agg_circuit_statistics**
   - Join: `circuit_name` (Many to One)
   - Cross filter: Single

---

## 📈 Suggested DAX Measures

### Core Measures

```dax
// Total Wins
Total Wins = 
COUNTROWS(
    FILTER(fact_race_results, fact_race_results[is_winner] = TRUE)
)

// Win Rate
Win Rate % = 
DIVIDE(
    [Total Wins],
    COUNTROWS(fact_race_results),
    0
) * 100

// Total Points
Total Points = SUM(fact_race_results[points_earned])

// Average Finish Position
Avg Finish Position = 
AVERAGE(fact_race_results[finish_position])

// Podium Count
Podium Count = 
COUNTROWS(
    FILTER(fact_race_results, fact_race_results[is_podium] = TRUE)
)

// Podium Rate
Podium Rate % = 
DIVIDE(
    [Podium Count],
    COUNTROWS(fact_race_results),
    0
) * 100

// Points Per Race
Points Per Race = 
DIVIDE(
    [Total Points],
    COUNTROWS(fact_race_results),
    0
)

// DNF Count
DNF Count = 
COUNTROWS(
    FILTER(
        fact_race_results, 
        fact_race_results[status_category] <> "Finished" && 
        fact_race_results[status_category] <> "Lapped"
    )
)

// DNF Rate
DNF Rate % = 
DIVIDE(
    [DNF Count],
    COUNTROWS(fact_race_results),
    0
) * 100
```

### Advanced Measures

```dax
// Year-over-Year Points Change
YoY Points Change = 
VAR CurrentYear = MAX(fact_race_results[race_year])
VAR CurrentPoints = 
    CALCULATE(
        [Total Points],
        fact_race_results[race_year] = CurrentYear
    )
VAR PreviousPoints = 
    CALCULATE(
        [Total Points],
        fact_race_results[race_year] = CurrentYear - 1
    )
RETURN
    CurrentPoints - PreviousPoints

// Running Championship Points
Running Championship Points = 
CALCULATE(
    [Total Points],
    FILTER(
        ALL(fact_race_results[race_round]),
        fact_race_results[race_round] <= MAX(fact_race_results[race_round])
    )
)

// Positions Gained/Lost
Avg Positions Gained = 
AVERAGE(fact_race_results[positions_gained])

// Home Race Flag
Is Home Race = 
IF(
    fact_race_results[driver_nationality] = fact_race_results[circuit_country],
    "Home Race",
    "Away Race"
)
```

---

## 📊 Dashboard Design Recommendations

### Page 1: Executive Summary
- **KPI Cards**: Total Races, Total Drivers, Total Constructors
- **Line Chart**: Points trend by year
- **Bar Chart**: Top 10 drivers by wins
- **Map Visual**: Circuits by country

### Page 2: Driver Analysis
- **Slicer**: Driver Name, Nationality, Year Range
- **Clustered Bar**: Wins, Podiums, Poles comparison
- **Line Chart**: Season-by-season performance
- **Table**: Career statistics

### Page 3: Constructor Analysis
- **Slicer**: Constructor Name, Year Range
- **Stacked Bar**: Points by constructor over years
- **Pie Chart**: Win distribution by constructor
- **Matrix**: Season-by-season results

### Page 4: Race Analysis
- **Slicer**: Race Year, Circuit
- **Table**: Race results with conditional formatting
- **Scatter Plot**: Grid Position vs Finish Position
- **Bar Chart**: DNF reasons distribution

### Page 5: Championship Tracker
- **Line Chart**: Championship points progression
- **Table**: Current standings
- **Card**: Championship Leader
- **Gauge**: Points gap to leader

---

## 🎨 Visualization Best Practices

### Color Theme (F1 Inspired)
```
Primary:        #E10600 (F1 Red)
Secondary:      #15151E (Dark Navy)
Accent 1:       #FFFFFF (White)
Accent 2:       #38383F (Gray)
Background:     #15151E (Dark)
Card Background: #1E1E28
```

### Typography
- **Headers**: Segoe UI Bold, 16pt
- **Body**: Segoe UI, 12pt
- **Data Labels**: Segoe UI, 10pt

### Conditional Formatting Ideas
- **Positions Gained**: Green gradient for positive, Red for negative
- **Winner Highlight**: Gold background for P1
- **Podium**: Bronze, Silver, Gold colors for P1-P3

---

## 🔄 Refresh Schedule

### Power BI Service Setup

1. **Publish Report** to Power BI Service
2. **Configure Data Gateway** (if using on-premises)
3. **Set Dataset Refresh Schedule**:
   - Daily: For active season data
   - Weekly: For historical analysis

### Incremental Refresh (Optional)

```
Configure incremental refresh on fact_race_results:
- Store data for: 5 years
- Refresh data for: 1 year
- Partition by: race_date or race_year
```

---

## 📱 Mobile Optimization

1. Create **Phone Layout** in Power BI Desktop
2. Key visuals to prioritize:
   - Championship standings card
   - Latest race results
   - Quick stats (wins, podiums)
3. Use collapsible slicers

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Connection timeout | Increase timeout in connection settings |
| Slow queries | Use Import mode instead of DirectQuery |
| Missing data | Check table refresh in Databricks |
| Relationship errors | Verify key columns match data types |

### Performance Tips

1. **Filter early**: Apply filters in Power Query before loading
2. **Remove unused columns**: Only import needed columns
3. **Use aggregations**: Prefer Gold layer over Silver for large datasets
4. **Enable query folding**: Let Databricks handle filtering

---

## 📚 Sample Queries for Power BI

### Top 10 Drivers by Wins (Current Season)
```sql
SELECT 
    driver_name,
    COUNT(*) as wins
FROM f1_gold.fact_race_results
WHERE is_winner = TRUE
    AND race_year = YEAR(CURRENT_DATE())
GROUP BY driver_name
ORDER BY wins DESC
LIMIT 10
```

### Championship Progression
```sql
SELECT 
    race_round,
    driver_name,
    SUM(points_earned) OVER (
        PARTITION BY driver_id, race_year 
        ORDER BY race_round
    ) as cumulative_points
FROM f1_gold.fact_race_results
WHERE race_year = 2023
ORDER BY race_round, cumulative_points DESC
```

---

## ✅ Checklist Before Publishing

- [ ] All data relationships are configured
- [ ] Date table is created for time intelligence
- [ ] Measures are organized in a Measures table
- [ ] Column formatting is applied (numbers, dates)
- [ ] Slicers have default values
- [ ] Report theme is applied
- [ ] Mobile layout is configured
- [ ] Refresh schedule is set

---

## 🎯 Quick Start Template

1. Connect to `f1_gold` database
2. Import these essential tables:
   - `fact_race_results`
   - `dim_driver_career`
   - `dim_constructor_performance`
3. Create relationships on ID columns
4. Add the core DAX measures
5. Build your first visual: Driver wins bar chart

Happy visualizing! 🏁
