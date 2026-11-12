SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49+ months'
    END AS tenure_group,

    COUNT(*) AS total_customers,

    SUM(
        CASE WHEN Churn = 'Yes' THEN 1
        ELSE 0 END
    ) AS churned_customers,

    ROUND(
        100.0 * SUM(
            CASE WHEN Churn = 'Yes' THEN 1
            ELSE 0 END
        ) / COUNT(*),
        2
    ) AS churn_percentage

FROM Customers

GROUP BY tenure_group

ORDER BY MIN(tenure);