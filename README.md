# E-commerce Sales Analytics

## Project Overview

This project demonstrates an end-to-end data analytics and ETL workflow for an e-commerce sales dataset.

The project starts with raw transactional CSV files and applies data profiling, quality assessment, cleaning, validation, relational database modeling, and SQL-based business analysis.

The main objective is to transform raw operational data into a clean and structured analytical database and extract meaningful business insights from customers, products, orders, order items, and payments.

---

## Project Workflow

```text
Raw CSV Data
     ↓
Data Profiling
     ↓
Data Quality Assessment
     ↓
Data Cleaning & Transformation
     ↓
Data Validation
     ↓
Relational Database Creation
     ↓
Data Loading
     ↓
SQL Analysis
     ↓
Business Insights
```

---

## Dataset

The project contains five related datasets:

| Dataset           | Description                                                             |
| ----------------- | ----------------------------------------------------------------------- |
| `customers.csv`   | Customer information, demographics, segmentation, and registration data |
| `products.csv`    | Product information, categories, pricing, brands, and suppliers         |
| `orders.csv`      | Order-level transaction and operational information                     |
| `order_items.csv` | Product-level details for each order                                    |
| `payments.csv`    | Payment dates, methods, statuses, and amounts                           |

The datasets represent a relational e-commerce environment where customer, product, order, and payment data are connected through primary and foreign-key relationships.

The raw datasets are provided in `data.zip`.

---

## Data Model

The main relationships between the datasets are:

```text
Customers
    │
    └──< Orders
             │
             ├──< Order Items >── Products
             │
             └──< Payments
```

This structure allows customer-level, order-level, product-level, and payment-level analysis.

---

## ETL Pipeline

The main ETL workflow is implemented in:

`ETL_Pipeline.py`

The pipeline performs the following steps:

### 1. Data Ingestion

Raw CSV files are loaded into pandas DataFrames.

### 2. Data Profiling

The datasets are initially profiled to identify:

* Number of records
* Column structure
* Missing values
* Duplicate records
* Data types
* Categorical distributions
* Numerical statistics

### 3. Data Quality Assessment

The pipeline checks for potential data-quality issues including:

* Duplicate records
* Duplicate customer IDs
* Missing values
* Invalid dates
* Negative monetary values
* Zero or negative quantities
* Negative unit prices

### 4. Referential Integrity Validation

Relationships between tables are validated before loading the data into the database.

The following relationships are checked:

```text
Orders → Customers
Order Items → Orders
Order Items → Products
Payments → Orders
```

This helps identify orphan records and prevents invalid relationships from entering the relational database.

### 5. Data Cleaning

The cleaning process includes:

* Converting date fields to datetime
* Removing duplicate records
* Handling missing categorical values
* Handling missing payment methods
* Treating missing discounts as zero
* Removing order items with missing quantities
* Removing invalid quantities
* Removing negative unit prices
* Resolving duplicated customer IDs

### 6. Data Validation

Critical business and structural rules are validated using explicit checks and assertions before database loading.

---

## Relational Database

The cleaned datasets are loaded into a SQLite relational database.

The database contains the following tables:

```text
customers
products
orders
order_items
payments
```

The database schema is defined in:

`schema.sql`

Primary keys and foreign keys are used to represent relationships between the tables.

SQLite foreign-key enforcement is enabled during database creation.

---

## SQL Analysis

The project includes several SQL-based business analyses.

### 1. Order Status Analysis

The distribution of orders across different statuses is analyzed to provide an overview of the order lifecycle.

### 2. Top 10 Customers by Sales

Customers are ranked according to total realized sales.

The calculation is based on:

```text
Quantity × Unit Price × (1 − Discount %)
```

Only `delivered` and `completed` orders are included in the calculation.

### 3. Top 3 Products per Category

Products are ranked within each category based on realized sales.

The analysis uses a SQL window function:

```sql
ROW_NUMBER() OVER (
    PARTITION BY category
    ORDER BY total_sales DESC
)
```

This demonstrates group-level ranking using SQL window functions.

### 4. Order and Payment Status Consistency

Potential inconsistencies between order and payment statuses are identified.

Examples include:

```text
Cancelled Order + Paid Payment
Returned Order + Paid Payment
Delivered Order + Failed Payment
```

These checks can help identify operational issues or potential data-quality problems.

### 5. Sales by Product Category

Total realized sales are aggregated by product category to compare category-level performance.

---

## Key SQL Concepts Demonstrated

The SQL analysis includes:

* `JOIN`
* `GROUP BY`
* `ORDER BY`
* Aggregate functions
* `WHERE`
* Common Table Expressions (CTEs)
* Window functions
* `ROW_NUMBER()`
* Conditional filtering
* Foreign-key validation

The main analytical queries are available in:

`queries.sql`

---

## Project Files

```text
E-commerce-Sales-Analytics/
│
├── README.md
├── ETL_Pipeline.py
├── Report.md
├── queries.sql
├── schema.sql
├── requirements.txt
└── data.zip
```

### File Description

| File               | Purpose                                   |
| ------------------ | ----------------------------------------- |
| `ETL_Pipeline.py`  | Main Python ETL and data-quality pipeline |
| `schema.sql`       | Relational database schema                |
| `queries.sql`      | Main analytical SQL queries               |
| `Report.md`        | Detailed analysis and findings            |
| `requirements.txt` | Python dependencies                       |
| `data.zip`         | Raw CSV datasets                          |

---

## Technologies

* Python
* Pandas
* SQL
* SQLite
* Jupyter Notebook / Google Colab
* Git
* GitHub

---

## Skills Demonstrated

### Data Analytics

* Data profiling
* Exploratory data analysis
* Data cleaning
* Missing-value handling
* Duplicate detection
* Business-rule validation
* Data-quality analysis

### SQL

* Relational joins
* Aggregation
* CTEs
* Window functions
* Ranking
* Data-quality queries
* Referential integrity validation

### Data Engineering Fundamentals

* ETL pipeline development
* Relational data modeling
* Primary and foreign keys
* Data validation
* Database creation
* Loading structured data into a relational database

---

## Reproducibility

To reproduce the project:

1. Download or clone the repository.
2. Extract `data.zip`.
3. Install the required Python dependency:

```bash
pip install -r requirements.txt
```

4. Update the input file paths in `ETL_Pipeline.py` if necessary.
5. Run the Python pipeline.
6. The pipeline performs the data preparation and database-loading process.
7. The SQL queries in `queries.sql` can then be executed against the resulting database.

---

## Future Improvements

Possible extensions of the project include:

* Customer RFM segmentation
* Customer retention analysis
* Monthly and quarterly sales trends
* Sales-channel performance analysis
* Product profitability analysis
* Payment conversion analysis
* Automated data-quality testing
* Migration from SQLite to SQL Server
* Automated scheduled ETL execution
* BI dashboard development

---

## Disclaimer

This project is developed for portfolio and educational purposes.

The dataset is intended to represent an e-commerce business environment and is used to demonstrate practical data analytics, ETL, SQL, and data-quality concepts.

```
```
