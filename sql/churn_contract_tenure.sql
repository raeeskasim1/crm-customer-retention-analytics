
WITH customer_groups AS (
    SELECT
        c.customerID,
        c.Churn,
        ct.Contract,

        CASE
            WHEN c.tenure <= 12 THEN '0-12 months'
            WHEN c.tenure <= 24 THEN '13-24 months'
            WHEN c.tenure <= 48 THEN '25-48 months'
            ELSE '49+ months'
        END AS tenure_group,

        CASE
            WHEN c.tenure <= 12 THEN 1
            WHEN c.tenure <= 24 THEN 2
            WHEN c.tenure <= 48 THEN 3
            ELSE 4
        END AS tenure_order

    FROM Customers c
    JOIN Contracts ct
        ON c.customerID = ct.customerID
)

SELECT
    tenure_group,
    Contract,
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

FROM customer_groups

GROUP BY tenure_group, tenure_order, Contract

ORDER BY tenure_order, churn_percentage DESC;
