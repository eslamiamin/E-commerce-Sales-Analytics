# E-commerce Sales Analytics

## Project Overview

This project demonstrates an end-to-end data analytics workflow for an e-commerce sales dataset.

The project covers the complete process from raw data ingestion and data quality assessment to data cleaning, relational database creation, and SQL-based business analysis.

The main objective is to transform raw transactional data into a structured analytical dataset and answer practical business questions related to customers, products, sales performance, and payment consistency.

---

## Business Questions

The analysis focuses on several practical business questions:

* Which customers generate the highest total sales?
* Which products perform best within each product category?
* How are orders distributed across different statuses?
* Are there inconsistencies between order status and payment status?
* Which product categories generate the highest sales?
* Does the transactional data satisfy basic data quality and referential integrity requirements?

---

## Dataset

The project uses five related datasets:

| Dataset       | Description                                          |
| ------------- | ---------------------------------------------------- |
| `customers`   | Customer demographic and registration information    |
| `products`    | Product, category, pricing, and supplier information |
| `orders`      | Order-level transactional information                |
| `order_items` | Product-level details for each order                 |
| `payments`    | Payment status, method, date, and amount             |

The datasets form a relational structure similar to a real-world e-commerce database.

### Data Model

The main relationships are:

```text
customers
    │
    └──< orders
             │
             ├──< order_items >── products
             │
             └──< payments
```

---

## Workflow

The project follows the following analytical pipeline:

```text
Raw CSV Files
      ↓
Data Loading
      ↓
Data Profiling
      ↓
Data Quality Assessment
      ↓
Data Cleaning
      ↓
Referential Integrity Validation
      ↓
SQLite Database
      ↓
SQL Analysis
      ↓
Business Insights
```

---

## 1. Data Loading

The raw CSV files are loaded into pandas DataFrames.

The initial inspection includes:

* Row and column counts
* Column names
* Missing values
* Duplicate records
* Data types
* Categorical value distributions
* Numerical statistics

---

## 2. Data Quality Assessment

Several data quality checks are performed before analytical processing.

### Duplicate Detection

Duplicate records are identified in customer and order-item data.

Customer IDs are also checked separately because a duplicated customer ID can violate the expected primary-key structure.

### Missing Values

Missing values are analyzed across all datasets.

Categorical missing values are handled using an `Unknown` category where appropriate.

For example:

```text
gender → Unknown
city → Unknown
province → Unknown
acquisition_channel → Unknown
payment_method → Unknown
```

Missing discounts are interpreted as zero discount.

### Invalid Values

Business-rule validation is applied to transactional fields.

Examples include:

* Non-positive quantities
* Negative unit prices
* Negative order amounts
* Negative payment amounts

Invalid order-item quantities and negative prices are removed before analytical processing.

---

## 3. Date Standardization

Date fields are converted into pandas datetime format.

Invalid date values are converted to `NaT` using:

```python
pd.to_datetime(..., errors="coerce")
```

The project then investigates missing dates by business status to determine whether missing values may be related to specific operational states.

---

## 4. Referential Integrity

Relationships between transactional and master data are validated before creating the database.

Examples:

```text
Orders → Customers
Order Items → Orders
Order Items → Products
Payments → Orders
```

This prevents orphan records from entering the relational database.

---

## 5. SQLite Database

After cleaning, the datasets are loaded into a relational SQLite database.

The database contains five tables:

```text
customers
products
orders
order_items
payments
```

Primary keys and foreign keys are defined to represent the relationships between the tables.

SQLite foreign-key enforcement is also enabled during the database creation process.

---

## 6. SQL Analysis

The project includes several analytical SQL queries.

### Top 10 Customers by Total Sales

Customer sales are calculated using order-item level data:

```text
Quantity × Unit Price × (1 − Discount %)
```

Only `delivered` and `completed` orders are included.

The query identifies the ten customers generating the highest realized sales.

---

### Top 3 Products per Category

Products are ranked within each category using the SQL window function:

```sql
ROW_NUMBER() OVER (
    PARTITION BY category
    ORDER BY total_sales DESC
)
```

This demonstrates the use of SQL window functions for group-level ranking.

---

### Order and Payment Status Inconsistencies

The project identifies potentially inconsistent combinations such as:

```text
Cancelled order + Paid payment
Returned order + Paid payment
Delivered order + Failed payment
```

These cases can be useful for identifying operational issues or potential data-quality problems.

---

### Sales by Product Category

Total realized sales are aggregated by product category to provide a high-level view of category performance.

---

## Technologies

* Python
* Pandas
* SQLite
* SQL
* Jupyter Notebook / Google Colab
* Git / GitHub

---

## Project Structure

```text
Yootab-Sales-Analytics/
│
├── README.md
├── analysis/
│   └── yootab_sales_analysis.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── database/
│   └── database1.db
│
├── data/
│   └── README.md
│
├── requirements.txt
└── .gitignore
```

---

## Key Skills Demonstrated

### Data Analytics

* Data profiling
* Data cleaning
* Missing-value handling
* Duplicate detection
* Business-rule validation
* Exploratory data analysis

### SQL

* Multi-table joins
* Aggregations
* `GROUP BY`
* `ORDER BY`
* Common Table Expressions (CTEs)
* Window functions
* Ranking
* Relational integrity checks

### Data Engineering Fundamentals

* Relational data modeling
* Primary and foreign keys
* Data validation
* Loading structured data into a database
* Reproducible database creation

---

## Reproducibility

The project is designed as a reproducible analytical workflow.

The Python script performs the following steps:

1. Loads the raw datasets.
2. Profiles the data.
3. Identifies data-quality issues.
4. Cleans and validates the datasets.
5. Creates the SQLite database.
6. Loads the cleaned data.
7. Executes analytical SQL queries.
8. Validates the resulting database.

---

## Future Improvements

Potential extensions of this project include:

* Customer segmentation using RFM analysis
* Monthly and quarterly sales trends
* Customer retention and repeat-purchase analysis
* Product profitability analysis
* Sales-channel performance comparison
* Payment conversion analysis
* Automated data-quality tests
* Interactive BI dashboard
* Migration from SQLite to SQL Server
* Development of an automated ETL pipeline

---

## Disclaimer

This project is intended for portfolio and educational purposes.

The analytical workflow is designed to demonstrate practical data analytics, SQL, and data-quality concepts using an e-commerce-style relational dataset.
