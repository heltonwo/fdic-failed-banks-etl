-- =============================================================================
-- Script:      01_eda.sql
-- Description: Exploratory queries that mirror the metrics shown in the
--              Power BI and Streamlit dashboards.
-- Expected:    Total failed banks and states affected match the dashboard KPIs
--              (578 and 44 at the time of the first load).
-- =============================================================================

-- 1. Total failed banks
SELECT COUNT(*) AS total_failed_banks
FROM failed_banks;

-- 2. States affected
SELECT COUNT(DISTINCT state) AS states_affected
FROM failed_banks;

-- 3. Top 10 acquiring institutions ("No Acquirer" is a value in the source data)
SELECT
    acquiring_institution,
    COUNT(*) AS failed_banks
FROM failed_banks
GROUP BY acquiring_institution
ORDER BY failed_banks DESC
LIMIT 10;

-- 4. Geographic distribution (top 10 states)
SELECT
    state,
    COUNT(*) AS failed_banks
FROM failed_banks
GROUP BY state
ORDER BY failed_banks DESC
LIMIT 10;

-- 5. Annual trend
SELECT
    closing_year,
    COUNT(*) AS failed_banks
FROM failed_banks
GROUP BY closing_year
ORDER BY closing_year;

-- 6. Seasonality pattern (by month)
SELECT
    closing_month,
    COUNT(*) AS failed_banks
FROM failed_banks
GROUP BY closing_month
ORDER BY closing_month;