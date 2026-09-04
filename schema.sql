schema_sql = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    gender TEXT,
    birth_year INTEGER,
    city TEXT,
    province TEXT,
    segment TEXT,
    registration_date DATE,
    acquisition_channel TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    brand TEXT,
    unit_cost REAL,
    list_price REAL,
    supplier TEXT,
    is_active INTEGER
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    status TEXT,
    channel TEXT,
    shipping_city TEXT,
    shipping_fee REAL,
    order_total_declared REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity REAL,
    unit_price REAL,
    discount_percent REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS payments (
    order_id INTEGER,
    payment_date DATE,
    payment_status TEXT,
    payment_method TEXT,
    paid_amount REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
"""

with open("schema.sql", "w", encoding="utf-8") as f:
    f.write(schema_sql)

print("schema.sql created.")