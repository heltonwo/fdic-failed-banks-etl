-- =============================================================================
-- Script:      02_data_quality.sql
-- Description: Data quality validation suite for the failed_banks table.
--              Covers row counts, completeness, duplicate detection,
--              and temporal boundary checks.
-- =============================================================================

-- =============================================================================
-- 1. Baseline Row Count Validation
-- =============================================================================
SELECT COUNT(*) AS total_rows
FROM failed_banks;

-- ========================================================================
-- 2. Completeness / Null Checks
-- Description: Checks data completeness across all primary columns by 
--              calculating missing/null value counts.
--=========================================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(bank_name) AS null_bank_name,
    COUNT(*) - COUNT(city) AS null_city,
    COUNT(*) - COUNT(state) AS null_state,
    COUNT(*) - COUNT(cert) AS null_cert,
    COUNT(*) - COUNT(acquiring_institution) AS null_acquiring_institution,
    COUNT(*) - COUNT(closing_date) AS null_closing_date,
    COUNT(*) - COUNT(fund) AS null_fund
FROM failed_banks;

-- =============================================================================
-- 3. Uniqueness / Duplicate Checks
-- Description: Identifies potential duplicate records using primary identifier (cert)
--              and composite business keys (bank_name, city, state, closing_date).
--==================================================================================
 
-- 1. Primary check by FDIC certificate number
SELECT
    cert,
    COUNT(*) AS occurrences
FROM failed_banks
GROUP BY cert
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;


-- 2. Secondary check by composite business keys

SELECT
    bank_name,
    city,
    state,
    closing_date,
    COUNT(*) AS occurrences
FROM failed_banks
GROUP BY
    bank_name,
    city,
    state,
    closing_date
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;

-- =============================================================================
-- 4. Validity / Temporal Boundary Checks
-- Description: Validates temporal boundaries and checks for invalid/null closing dates.
--===================================================================================


-- Boundary validation
SELECT
    MIN(closing_date) AS first_failure,
    MAX(closing_date) AS last_failure
FROM failed_banks;


-- Null date validation
SELECT COUNT(*) AS invalid_dates
FROM failed_banks
WHERE closing_date IS NULL;