
SELECT
    s.InternetService,
    COUNT(*) AS total_customers,

    SUM(
        CASE
            WHEN c.Churn = 'Yes' THEN 1
            ELSE 0
        END
    ) AS churned_customers,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN c.Churn = 'Yes' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS churn_percentage

FROM Customers c

JOIN Services s
    ON c.customerID = s.customerID

GROUP BY s.InternetService

ORDER BY churn_percentage DESC;
