```python
# ============================================================
# 1. LOAD RAW DATASETS
# ============================================================
# Load the raw CSV files into pandas DataFrames.
# Each file represents a major entity in the e-commerce dataset.

df_customers = pd.read_csv('data/customers.csv')
df_items = pd.read_csv('data/order_items.csv')
df_orders = pd.read_csv('data/orders.csv')
df_products = pd.read_csv('data/products.csv')
df_payments = pd.read_csv('data/payments.csv')


# ============================================================
# 2. INITIAL DATA QUALITY CHECK
# ============================================================
# Perform a first-level data quality assessment for each dataset.
# The checks include:
# - Number of rows
# - Available columns
# - Missing values
# - Duplicate rows

for name, df in {
    'customers': df_customers,
    'products': df_products,
    'orders': df_orders,
    'order_items': df_items,
    'payments': df_payments
}.items():
    print(f"\n {name}")
    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())
    print("\nMissing values:")
    print(df.isnull().sum())
    print("Duplicates:", df.duplicated().sum())


# Check duplicated customer records while keeping all duplicate occurrences.
# Sorting by customer_id makes potentially duplicated records easier to compare.
df_customers[df_customers.duplicated(keep=False)].sort_values('customer_id')


# Check duplicated order-item records based on the complete row.
# Sorting by order_id and product_id helps identify repeated line items.
df_items[df_items.duplicated(keep=False)].sort_values(['order_id', 'product_id'])


# ============================================================
# 3. CATEGORICAL DATA PROFILING
# ============================================================
# Inspect the distribution of key categorical variables.
# dropna=False is used to make missing values visible in the analysis.

print("Gender:")
print(df_customers['gender'].value_counts(dropna=False))

print("\nSegment:")
print(df_customers['segment'].value_counts(dropna=False))

print("\nOrder Status:")
print(df_orders['status'].value_counts(dropna=False))

print("\nOrder Channel:")
print(df_orders['channel'].value_counts(dropna=False))

print("\nPayment Status:")
print(df_payments['payment_status'].value_counts(dropna=False))

print("\nPayment Method:")
print(df_payments['payment_method'].value_counts(dropna=False))

print("\nProduct Category:")
print(df_products['category'].value_counts(dropna=False))


# ============================================================
# 4. NUMERICAL DATA PROFILING
# ============================================================
# Generate descriptive statistics for key numerical fields.
# This helps identify unusual values, outliers, and unexpected ranges.

print("Products:")
print(df_products[['unit_cost', 'list_price']].describe())

print("\nOrder Items:")
print(df_items[['quantity', 'unit_price', 'discount_percent']].describe())

print("\nOrders:")
print(df_orders[['shipping_fee', 'order_total_declared']].describe())

print("\nPayments:")
print(df_payments[['paid_amount']].describe())


# ============================================================
# 5. BUSINESS RULE VALIDATION
# ============================================================
# Identify values that violate basic business rules.
# Quantities should be positive, while prices and monetary amounts
# should not be negative.

print("Negative / zero quantities:")
print(df_items[df_items['quantity'] <= 0])

print("Negative unit prices:")
print(df_items[df_items['unit_price'] < 0])

print("Negative order/payment amounts:")
print("Orders:")
print(df_orders[df_orders['order_total_declared'] < 0])

print("\nPayments:")
print(df_payments[df_payments['paid_amount'] < 0])


# ============================================================
# 6. DATA TYPE INSPECTION
# ============================================================
# Review column data types before further transformation.
# Correct data types are particularly important for dates,
# numerical calculations, and database loading.

print("DATA TYPES")

for name, df in {
    "customers": df_customers,
    "products": df_products,
    "orders": df_orders,
    "order_items": df_items,
    "payments": df_payments
}.items():
    print(f"\n{name}")
    print(df.dtypes)


# ============================================================
# 7. REFERENTIAL INTEGRITY CHECK
# ============================================================
# Validate relationships between parent and child tables.
# These checks identify orphan records whose foreign-key values
# do not exist in the corresponding parent table.

print("REFERENTIAL INTEGRITY")


# Orders must reference an existing customer.
orphan_orders_customers = ~df_orders["customer_id"].isin(
    df_customers["customer_id"]
)
print("Orders with invalid customer_id:", orphan_orders_customers.sum())


# Order items must reference an existing order.
orphan_items_orders = ~df_items["order_id"].isin(
    df_orders["order_id"]
)
print("Order items with invalid order_id:", orphan_items_orders.sum())


# Order items must reference an existing product.
orphan_items_products = ~df_items["product_id"].isin(
    df_products["product_id"]
)
print("Order items with invalid product_id:", orphan_items_products.sum())


# Payments must reference an existing order.
orphan_payments_orders = ~df_payments["order_id"].isin(
    df_orders["order_id"]
)
print("Payments with invalid order_id:", orphan_payments_orders.sum())


# ============================================================
# 8. DATE STANDARDIZATION
# ============================================================
# Convert date columns from raw text/object format into pandas datetime.
# errors="coerce" converts invalid date values into NaT,
# allowing them to be identified and handled explicitly.

df_customers["registration_date"] = pd.to_datetime(
    df_customers["registration_date"],
    errors="coerce"
)

df_orders["order_date"] = pd.to_datetime(
    df_orders["order_date"],
    errors="coerce"
)

df_payments["payment_date"] = pd.to_datetime(
    df_payments["payment_date"],
    errors="coerce"
)


# ============================================================
# 9. DUPLICATE REMOVAL
# ============================================================
# Remove exact duplicate rows from customers and order items.
# Row counts are stored before and after cleaning to quantify
# the impact of the transformation.

before_customers = len(df_customers)
before_items = len(df_items)

df_customers = df_customers.drop_duplicates()
df_items = df_items.drop_duplicates()

print("Removed duplicate customers:", before_customers - len(df_customers))
print("Removed duplicate order items:", before_items - len(df_items))


# ============================================================
# 10. INVALID DATE ANALYSIS
# ============================================================
# Count records where date conversion failed.
# These records require additional investigation before being used
# in time-based analysis.

print("\nInvalid customer dates:",
      df_customers["registration_date"].isna().sum())

print("Invalid order dates:",
      df_orders["order_date"].isna().sum())

print("Invalid payment dates:",
      df_payments["payment_date"].isna().sum())


# Extract raw invalid date values for further investigation.
invalid_order_dates = df_orders[
    pd.to_datetime(df_orders["order_date"], errors="coerce").isna()
]["order_date"]

invalid_payment_dates = df_payments[
    pd.to_datetime(df_payments["payment_date"], errors="coerce").isna()
]["payment_date"]


# Display the most common invalid date values.
print("Invalid Order Dates")
print(invalid_order_dates.value_counts(dropna=False).head(20))

print("\n Invalid Payment Dates")
print(invalid_payment_dates.value_counts(dropna=False).head(20))


# Inspect raw date values to understand the original formatting.
print("Raw order_date examples:")
print(df_orders["order_date"].drop_duplicates().head(20).tolist())

print("\nRaw payment_date examples:")
print(df_payments["payment_date"].drop_duplicates().head(20).tolist())


# ============================================================
# 11. INVESTIGATE MISSING DATES BY BUSINESS STATUS
# ============================================================
# Analyze missing dates in the context of business status.
# This helps determine whether missing dates are random or related
# to specific operational states.

print("Orders: Missing order_date by status")

print(
    df_orders[df_orders["order_date"].isna()]["status"]
    .value_counts(dropna=False)
)

print("\n Payments: Missing payment_date by status ")

print(
    df_payments[df_payments["payment_date"].isna()]["payment_status"]
    .value_counts(dropna=False)
)


# Inspect individual orders with missing order dates.
print("Orders with missing order_date")

print(
    df_orders[df_orders["order_date"].isna()][
        ["order_id", "customer_id", "status", "channel",
         "shipping_fee", "order_total_declared"]
    ].head(20)
)


# ============================================================
# 12. MISSING VALUE ANALYSIS
# ============================================================
# Re-check missing values after the initial cleaning steps.
# Only columns containing missing values are displayed.

print(" MISSING VALUES ")

for name, df in {
    "customers": df_customers,
    "products": df_products,
    "orders": df_orders,
    "order_items": df_items,
    "payments": df_payments
}.items():

    print(f"\n{name}")
    missing = df.isna().sum()
    print(missing[missing > 0])


# ============================================================
# 13. MISSING VALUE HANDLING
# ============================================================
# Define replacement values for missing categorical attributes.
# "Unknown" is used instead of dropping these records because
# the absence of demographic information does not invalidate
# the customer record.

categorical_missing = {
    "gender": "Unknown",
    "city": "Unknown",
    "province": "Unknown",
    "acquisition_channel": "Unknown"
}

for col, value in categorical_missing.items():
    df_customers[col] = df_customers[col].fillna(value)


# Payment method is treated similarly because a missing method
# does not necessarily mean the payment record is invalid.
df_payments["payment_method"] = df_payments["payment_method"].fillna(
    "Unknown"
)


# Quantity is required for order-item calculations,
# so records without a quantity are removed.
df_items = df_items.dropna(subset=["quantity"])


# A missing discount is interpreted as no discount.
df_items["discount_percent"] = df_items["discount_percent"].fillna(0)


# ============================================================
# 14. REMOVE INVALID TRANSACTION VALUES
# ============================================================
# Remove order-item records that violate basic transaction rules.
# Quantity must be positive and unit price cannot be negative.

df_items = df_items[df_items["quantity"] > 0]
df_items = df_items[df_items["unit_price"] >= 0]


# ============================================================
# 15. POST-CLEANING VALIDATION
# ============================================================
# Compare dataset sizes after the cleaning process.

print(" CLEANED DATASET SIZES ")

for name, df in {
    "customers": df_customers,
    "products": df_products,
    "orders": df_orders,
    "order_items": df_items,
    "payments": df_payments
}.items():
    print(f"{name}: {len(df):,} rows")


# Confirm whether any missing values remain.
print("\nCustomers missing:")
print(df_customers.isna().sum()[df_customers.isna().sum() > 0])

print("\nOrders missing:")
print(df_orders.isna().sum()[df_orders.isna().sum() > 0])

print("\nOrder items missing:")
print(df_items.isna().sum()[df_items.isna().sum() > 0])

print("\nPayments missing:")
print(df_payments.isna().sum()[df_payments.isna().sum() > 0])


# Confirm that invalid transaction values have been removed.
print("\nInvalid quantities:", (df_items["quantity"] <= 0).sum())
print("Negative unit prices:", (df_items["unit_price"] < 0).sum())


# ============================================================
# 16. CUSTOMER ID UNIQUENESS VALIDATION
# ============================================================
# Check whether customer_id can safely be used as a primary key.

print("Total customers:", len(df_customers))
print("Unique customer IDs:", df_customers["customer_id"].nunique())
print("Duplicate customer IDs:",
      df_customers["customer_id"].duplicated().sum())


# Identify customers with duplicated IDs.
duplicate_customers = df_customers[
    df_customers["customer_id"].duplicated(keep=False)
].sort_values("customer_id")

print(duplicate_customers)


# ============================================================
# 17. INVESTIGATE DUPLICATE CUSTOMER RECORDS
# ============================================================
# Determine whether duplicated customer IDs are associated with
# existing orders before deciding which record to retain.

duplicate_ids = df_customers[
    df_customers["customer_id"].duplicated(keep=False)
]["customer_id"].unique()

for customer_id in duplicate_ids:
    order_count = (
        df_orders["customer_id"] == customer_id
    ).sum()

    print(
        f"customer_id = {customer_id} | "
        f"orders = {order_count}"
    )


# Display all records for each duplicated customer ID
# to support manual investigation.
for customer_id in duplicate_ids:
    print(f"\n===== {customer_id} =====")
    print(
        df_customers[
            df_customers["customer_id"] == customer_id
        ].T
    )


# ============================================================
# 18. DEDUPLICATE CUSTOMER MASTER DATA
# ============================================================
# Keep the first record for each customer_id.
# This ensures customer_id can be used as a unique primary key
# when the data is loaded into the SQL database.

df_customers = df_customers.drop_duplicates(
    subset=["customer_id"],
    keep="first"
).copy()


# Validate the final customer master table.
print("Customers after deduplication:", len(df_customers))
print("Unique customer IDs:", df_customers["customer_id"].nunique())
print("Duplicate customer IDs:",
      df_customers["customer_id"].duplicated().sum())


# ============================================================
# 19. FINAL DATA INTEGRITY ASSERTIONS
# ============================================================
# Use assertions to enforce critical data quality rules.
# The pipeline will stop if either condition is violated.

assert df_customers["customer_id"].is_unique

assert df_orders["customer_id"].isin(
    df_customers["customer_id"]
).all()


# ============================================================
# 20. CREATE SQLITE DATABASE
# ============================================================
# Create a fresh SQLite database for the cleaned datasets.
# The existing database file is removed to ensure a reproducible
# database build from the cleaned source data.

DB_PATH = Path("database1.db")

if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(DB_PATH)

# Enable SQLite foreign-key enforcement.
conn.execute("PRAGMA foreign_keys = ON;")

print("New database created.")


# ============================================================
# 21. DEFINE RELATIONAL DATABASE SCHEMA
# ============================================================
# Define the relational structure of the e-commerce database.
# Primary keys identify unique entities, while foreign keys enforce
# relationships between transactional and master tables.

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


# Execute the complete database schema and commit the transaction.
conn.executescript(schema_sql)
conn.commit()


# ============================================================
# 22. LOAD CLEANED DATA INTO SQLITE
# ============================================================
# Load the cleaned pandas DataFrames into their corresponding
# relational database tables.

df_customers.to_sql(
    "customers", conn, if_exists="append", index=False
)

df_products.to_sql(
    "products", conn, if_exists="append", index=False
)

df_orders.to_sql(
    "orders", conn, if_exists="append", index=False
)

df_items.to_sql(
    "order_items", conn, if_exists="append", index=False
)

df_payments.to_sql(
    "payments", conn, if_exists="append", index=False
)


# ============================================================
# 23. DATABASE ROW COUNT VALIDATION
# ============================================================
# Verify that the expected number of records were successfully
# loaded into each database table.

tables = [
    "customers",
    "products",
    "orders",
    "order_items",
    "payments"
]

for table in tables:
    result = pd.read_sql_query(
        f"SELECT COUNT(*) AS count FROM {table}",
        conn
    )

    print(table, ":", result.iloc[0]["count"])


# ============================================================
# 24. SQL ANALYSIS — ORDER STATUS DISTRIBUTION
# ============================================================
# Analyze the number of orders by status.
# This provides a high-level view of the operational order lifecycle.

query = """
SELECT
    status,
    COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;
"""

pd.read_sql_query(query, conn)


# ============================================================
# 25. SQL ANALYSIS — TOP 10 CUSTOMERS BY SALES
# ============================================================
# Calculate total realized sales for each customer using order-item
# level data.
#
# Only delivered and completed orders are included to avoid counting
# cancelled or otherwise unsuccessful transactions.
#
# Revenue is calculated after applying the item-level discount.

query = """
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
"""

top_10_customers = pd.read_sql_query(query, conn)

print("Top 10 Customers by Total Sales")
display(top_10_customers)


# ============================================================
# 26. SQL ANALYSIS — TOP 3 PRODUCTS BY CATEGORY
# ============================================================
# Calculate sales by product and rank products within each category.
# ROW_NUMBER() is used as a window function to assign a ranking
# independently within each product category.

query_top_products = """
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
"""

top_3_products = pd.read_sql_query(
    query_top_products,
    conn
)

print("Top 3 Products per Category")
display(top_3_products)


# ============================================================
# 27. SQL ANALYSIS — ORDER/PAYMENT STATUS INCONSISTENCIES
# ============================================================
# Identify potentially inconsistent combinations between order status
# and payment status.
#
# Examples include:
# - Cancelled orders with successful payments
# - Returned orders with completed payments
# - Delivered orders with failed payments
#
# These cases can indicate operational or data-quality issues.

query_status_inconsistencies = """
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

status_inconsistencies = pd.read_sql_query(
    query_status_inconsistencies,
    conn
)

print("Order/Payment Status Inconsistencies")
display(status_inconsistencies)


# ============================================================
# 28. EXPORT SQL ANALYSIS QUERIES
# ============================================================
# Store the main analytical SQL queries in a separate .sql file.
# Keeping SQL logic outside the Python notebook makes the project
# easier to review, reuse, and maintain on GitHub.

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


# Save the SQL queries as a standalone file for GitHub documentation.
with open("queries.sql", "w", encoding="utf-8") as f:
    f.write(queries_sql)

print("queries.sql saved successfully.")


# ============================================================
# 29. DATABASE VALIDATION
# ============================================================
# Perform a final database-level validation.
# Row counts confirm successful data loading, while foreign-key
# checks verify relational integrity.

tables = [
    "customers",
    "products",
    "orders",
    "order_items",
    "payments"
]

print("Row counts:")

for table in tables:
    count = pd.read_sql_query(
        f"SELECT COUNT(*) AS count FROM {table}",
        conn
    ).iloc[0]["count"]

    print(f"{table}: {count}")


print("\nForeign key violations:")

for table in tables:
    violations = pd.read_sql_query(
        f"PRAGMA foreign_key_check({table});",
        conn
    )

    print(f"{table}: {len(violations)} violations")


# ============================================================
# 30. EXPORT DATABASE SCHEMA
# ============================================================
# Save the database schema as a separate SQL file.
# This allows the database structure to be recreated without
# running the full Python data preparation pipeline.

with open("schema.sql", "w", encoding="utf-8") as f:
    f.write(schema_sql)


# ============================================================
# 31. DEFINE PROJECT DEPENDENCIES
# ============================================================
# Store the main Python dependency required to run the data
# preparation and analysis workflow.

requirements = """pandas"""

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write(requirements)


# ============================================================
# 32. SQL ANALYSIS — SALES BY PRODUCT CATEGORY
# ============================================================
# Calculate total realized sales for each product category.
# The result can be used for category-level performance analysis.

query = """
SELECT
    p.category,
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
GROUP BY p.category
ORDER BY total_sales DESC;
"""

category_sales = pd.read_sql_query(
    query,
    conn
)

category_sales
```
