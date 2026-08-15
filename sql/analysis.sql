-- ============================================================
-- HOSPITAL PIPELINE — Analytical Queries
-- Database: PostgreSQL (Airflow container)
-- Table: hospital_records
-- ============================================================


-- 1. Average cost by health service area
-- Which regions cost the most per hospitalization?
SELECT
    "Health Service Area",
    COUNT(*)                          AS total_records,
    ROUND(AVG("Total Costs")::numeric, 2)    AS avg_cost,
    ROUND(AVG("Total Charges")::numeric, 2)  AS avg_charges,
    ROUND(AVG("charge_cost_ratio")::numeric, 4) AS avg_ratio
FROM hospital_records
GROUP BY "Health Service Area"
ORDER BY avg_cost DESC;


-- 2. Charge-to-cost ratio by type of admission
-- Emergency admissions tend to be more expensive — is that true here?
SELECT
    "Type of Admission",
    COUNT(*)                                    AS total_records,
    ROUND(AVG("charge_cost_ratio")::numeric, 4) AS avg_ratio,
    ROUND(MIN("charge_cost_ratio")::numeric, 4) AS min_ratio,
    ROUND(MAX("charge_cost_ratio")::numeric, 4) AS max_ratio
FROM hospital_records
WHERE "charge_cost_ratio" IS NOT NULL
GROUP BY "Type of Admission"
ORDER BY avg_ratio DESC;


-- 3. Admissions by severity of illness
-- How many patients at each severity level?
SELECT
    "APR Severity of Illness Description",
    COUNT(*)                        AS total_records,
    ROUND(AVG("Total Costs")::numeric, 2) AS avg_cost
FROM hospital_records
WHERE "APR Severity of Illness Description" IS NOT NULL
GROUP BY "APR Severity of Illness Description"
ORDER BY total_records DESC;


-- 4. Top 10 most frequent diagnoses
-- What conditions are filling hospital beds?
SELECT
    "CCS Diagnosis Description",
    COUNT(*) AS total_records,
    ROUND(AVG("Total Costs")::numeric, 2) AS avg_cost
FROM hospital_records
GROUP BY "CCS Diagnosis Description"
ORDER BY total_records DESC
LIMIT 10;