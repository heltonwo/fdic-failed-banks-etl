-- =============================================================================
-- Script: 04_rankings.sql
-- Description: Extracts top 10 rankings for highest failure concentrations by year and state.
-- ============================================================================================


-- Top 10 years with most bank failures
SELECT
    closing_year,
    COUNT(*) AS failed_banks
FROM failed_banks
GROUP BY closing_year
ORDER BY failed_banks DESC
LIMIT 10;

-- Top 10 states with most bank failures

SELECT
    state,
    COUNT(*) AS failed_banks
FROM failed_banks
GROUP BY state
ORDER BY failed_banks DESC
LIMIT 10;