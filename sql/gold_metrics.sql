-- Example gold-layer query
SELECT
    order_date,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_revenue
FROM local.gold.daily_orders
GROUP BY order_date
ORDER BY order_date;
