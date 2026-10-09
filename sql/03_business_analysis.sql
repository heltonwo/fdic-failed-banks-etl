-- =============================================================================
-- Script: 03_business_analysis.sql
-- Description: Aggregates bank failures across core analytical dimensions
--              (Year, State, Acquiring Institution, Month).
--========================================================================

-- Aggregation by year
SELECT
    closing_year,
    COUNT(*) AS failed_banks
FROM failed_banks
GROUP BY closing_year
ORDER BY closing_year;

-- Aggregation by state
SELECT
    state,
    COUNT(*) AS failed_banks
FROM failed_banks
GROUP BY state
ORDER BY failed_banks DESC;

-- Aggregation by acquiring institution

SELECT
    acquiring_institution,
    COUNT(*) AS failed_banks
FROM failed_banks
GROUP BY acquiring_institution
ORDER BY failed_banks DESC;

-- Aggregation by year and month

SELECT
    closing_year,
    closing_month,
    COUNT(*) AS failed_banks
FROM failed_banks
GROUP BY
    closing_year,
    closing_month
ORDER BY
    closing_year,
    closing_month; 