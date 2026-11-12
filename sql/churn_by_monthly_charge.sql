WITH charge_groups AS (
    SELECT
        c.customerID,
        c.Churn,
        b.MonthlyCharges,

        CASE
            WHEN b.MonthlyCharges < 40 THEN 'Below 40'
            WHEN b.MonthlyCharges < 70 THEN '40-69.99'
            WHEN b.MonthlyCHarges < 100 THEN '70-99.99'
            ELSE '100+'
        END AS charge_group
    
    FROM Customers c
    JOIN Billing b
        ON c.customerID = b.customerID
)

SELECT
    charge_group,
    COUNT(*) AS total_customers,

    ROUND(AVG(MonthlyCharges), 2)
        AS average_monthly_charge,
    
    SUM(
        CASE WHEN Churn = 'Yes' THEN 1
        ELSE 0 END
    ) AS churned_customers,

    ROUND(
        100.0 * SUM(
            CASE WHEN CHurn = 'Yes' Then 1
            ELSE 0 END
        ) / COUNT(*),
        2
    ) AS churn_percentage

FROM charge_groups

GROUP BY charge_group

ORDER BY MIN(MonthlyCHarges);
