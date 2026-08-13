CREATE OR REPLACE TABLE gold_hr_attrition_metrics AS
SELECT 
    department,
    DATE_TRUNC('month', effective_start_date) AS report_month,
    COUNT(DISTINCT CASE WHEN status = 'Active' THEN employee_id END) AS active_headcount,
    COUNT(DISTINCT CASE WHEN status = 'Resigned' THEN employee_id END) AS resigned_headcount,
    ROUND(
        COUNT(DISTINCT CASE WHEN status = 'Resigned' THEN employee_id END) * 100.0 / 
        NULLIF(COUNT(DISTINCT employee_id), 0), 2
    ) AS attrition_rate_percentage
FROM silver_employee_history
GROUP BY 1, 2;

SELECT * FROM gold_hr_attrition_metrics 
ORDER BY report_month DESC, attrition_rate_percentage DESC;
