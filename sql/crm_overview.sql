
SELECT
    COUNT(*) AS total_customers,

    SUM(
        CASE WHEN c.Churn = 'Yes'
        THEN 1 ELSE 0 END
    ) AS churned_customers,

    SUM(
        CASE WHEN c.Churn = 'No'
        THEN 1 ELSE 0 END
    ) AS non_churned_customers,

    ROUND(
        100.0 * SUM(
            CASE WHEN c.Churn = 'Yes'
            THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS churn_percentage,

    ROUND(
        100.0 * SUM(
            CASE WHEN c.Churn = 'No'
            THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    ) AS non_churn_percentage,

    ROUND(AVG(b.MonthlyCharges), 2)
        AS avg_monthly_charge

FROM Customers c

JOIN Billing b
    ON c.customerID = b.customerID;
