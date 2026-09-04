queries_sql = """
-- Query 1: Top 10 Customers by Total Sales

SELECT
    c.customer_id,
    c.customer_name,
    SUM(
        oi.quantity
        * oi.unit_price
        * (1 - oi.discount_percent / 100.0)
    ) AS total_sales
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.status IN ('delivered', 'completed')
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_sales DESC
LIMIT 10;


-- Query 2: Top 3 Products per Category

WITH product_sales AS (
    SELECT
        p.category,
        p.product_id,
        p.product_name,
        SUM(
            oi.quantity
            * oi.unit_price
            * (1 - oi.discount_percent / 100.0)
        ) AS total_sales
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.status IN ('delivered', 'completed')
    GROUP BY
        p.category,
        p.product_id,
        p.product_name
),
ranked_products AS (
    SELECT
        category,
        product_id,
        product_name,
        total_sales,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY total_sales DESC
        ) AS rank
    FROM product_sales
)
SELECT
    category,
    product_id,
    product_name,
    total_sales,
    rank
FROM ranked_products
WHERE rank <= 3
ORDER BY
    category,
    rank;


-- Query 3: Order/Payment Status Inconsistencies

SELECT
    o.status AS order_status,
    p.payment_status,
    COUNT(*) AS order_count,
    SUM(p.paid_amount) AS total_paid_amount
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
WHERE
    (o.status = 'cancelled' AND p.payment_status IN ('paid', 'partially_paid'))
    OR
    (o.status = 'returned' AND p.payment_status = 'paid')
    OR
    (o.status = 'delivered' AND p.payment_status = 'failed')
GROUP BY
    o.status,
    p.payment_status
ORDER BY order_count DESC;
"""

with open("queries.sql", "w", encoding="utf-8") as f:
    f.write(queries_sql)

print("queries.sql created.")