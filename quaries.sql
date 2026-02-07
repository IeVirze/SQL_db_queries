-- Query 1 Funnel performance by Country and Channel
-- query assumes:
-- - date format is yyyy-mm-dd 
-- - multiple years are queried

SELECT 
    strftime('%Y-%m', app.date) as month,
    ch.channel_group as channel,
    con.country_name as country,
    COUNT(*) as total_applications,
    SUM(loan_amount) as total_loan_value,
    ROUND(AVG(loan_amount), 2) as avg_loan_amount
FROM dim_applications app 
JOIN dim_countries con ON app.country_id = con.id 
JOIN dim_channel ch ON app.channel_id = ch.id 
GROUP BY month
ORDER BY month DESC, total_loan_value DESC;

--Query 2 Channel quality vs volume trade-off

SELECT 
    ch.channel_group,
    COUNT(*) as total_applications,
    ROUND(AVG(a.loan_amount), 2) as avg_loan_amount,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM dim_applications), 2) as share_of_total
FROM dim_applications a
JOIN dim_channel ch ON a.channel_id = ch.id
GROUP BY ch.channel_group
HAVING share_of_total >= 10
ORDER BY share_of_total DESC;

--Query 3 Product-country performance

SELECT 
    p.product_short_name,
    c.country_name,
    COUNT(*) as num_applications,
    ROUND(SUM(a.loan_amount), 2) as total_loan_amount,
    ROUND(AVG(a.loan_amount), 2) as avg_loan_amount
FROM dim_applications a
JOIN dim_products p ON a.product_id = p.id
JOIN dim_countries c ON a.country_id = c.id
WHERE p.id IN (
    SELECT product_id
    FROM dim_applications
    GROUP BY product_id
    HAVING COUNT(*) >= 1000)
GROUP BY p.product_short_name, c.country_name
ORDER BY p.product_short_name, num_applications DESC