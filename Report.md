# E-commerce Sales Analytics — Data Quality & Business Analysis Report

## 1. Executive Summary

This project analyzes an e-commerce transactional dataset consisting of customer, product, order, order-item, and payment information.

The analysis follows an end-to-end data workflow, beginning with raw data inspection and quality assessment and continuing through data cleaning, relational database creation, and SQL-based business analysis.

The primary goals were:

1. Assess the quality and consistency of the raw datasets.
2. Identify and resolve data-quality issues.
3. Build a structured relational database.
4. Validate relationships between transactional and master data.
5. Answer practical business questions using SQL.
6. Produce a reproducible analytical workflow.

---

# 2. Data Structure

The dataset contains five main entities.

### Customers

Contains customer-level information such as:

* Customer ID
* Customer name
* Gender
* Birth year
* Location
* Customer segment
* Registration date
* Acquisition channel

### Products

Contains product master data including:

* Product ID
* Product name
* Category
* Brand
* Unit cost
* List price
* Supplier
* Active status

### Orders

Contains order-level information including:

* Order ID
* Customer ID
* Order date
* Order status
* Sales channel
* Shipping city
* Shipping fee
* Declared order total

### Order Items

Contains product-level details associated with each order:

* Order ID
* Product ID
* Quantity
* Unit price
* Discount percentage

### Payments

Contains payment information including:

* Order ID
* Payment date
* Payment status
* Payment method
* Paid amount

---

# 3. Data Quality Assessment

Before performing business analysis, the raw data was systematically profiled.

The following dimensions were assessed:

* Completeness
* Uniqueness
* Validity
* Consistency
* Referential integrity
* Data type correctness

This approach was used to prevent data-quality problems from propagating into downstream analysis.

---

# 4. Duplicate Records

Duplicate records were investigated at both the row level and key level.

Exact duplicate rows were identified in customer and order-item datasets.

Customer IDs were also checked separately because duplicate customer IDs can violate the expected primary-key structure of the customer master table.

Duplicate customer records were investigated before selecting the final record to retain.

The final customer table was validated to ensure that:

```text
customer_id IS UNIQUE
```

---

# 5. Missing Values

Missing values were assessed across all five datasets.

Different treatment strategies were applied depending on the business meaning of the field.

### Categorical Attributes

Missing categorical attributes such as demographic or location fields were assigned:

```text
Unknown
```

This preserves the underlying record while making the missing state explicit.

### Payment Method

Missing payment methods were also assigned:

```text
Unknown
```

### Discount

Missing discount percentages were interpreted as:

```text
0%
```

This assumes that a missing discount represents an order item without a recorded discount.

### Quantity

Quantity is essential for sales calculations.

Records without a valid quantity were therefore excluded from the order-item dataset.

---

# 6. Invalid Values

Several business-rule validations were performed.

### Quantity

Order-item quantity should be greater than zero.

Records satisfying:

```text
quantity <= 0
```

were removed.

### Unit Price

Unit price should not be negative.

Records satisfying:

```text
unit_price < 0
```

were removed.

### Monetary Amounts

Order totals and payment amounts were checked for negative values.

These records were flagged during the data-quality assessment for further investigation.

---

# 7. Date Validation

Date fields were converted from raw values into pandas datetime objects.

The following fields were processed:

```text
registration_date
order_date
payment_date
```

Invalid values were converted to `NaT` using error coercion.

Missing dates were then analyzed in relation to business statuses to determine whether missingness was concentrated in particular operational states.

This contextual analysis is important because simply replacing missing dates without understanding their business meaning can introduce incorrect assumptions into time-based analysis.

---

# 8. Referential Integrity

The relationships between master and transactional datasets were validated before loading the data into SQLite.

The following relationships were checked:

```text
orders.customer_id
        ↓
customers.customer_id
```

```text
order_items.order_id
        ↓
orders.order_id
```

```text
order_items.product_id
        ↓
products.product_id
```

```text
payments.order_id
        ↓
orders.order_id
```

The database also uses foreign-key constraints to enforce these relationships after loading.

---

# 9. Relational Database Design

After data cleaning and validation, the datasets were loaded into a SQLite relational database.

The database consists of:

```text
customers
products
orders
order_items
payments
```

The model separates master data from transactional data.

This structure supports analytical queries across multiple business dimensions while maintaining referential integrity.

The database schema is defined in:

```text
schema.sql
```

---

# 10. Sales Calculation Logic

For order-item level sales analysis, realized sales are calculated using:

```text
Quantity × Unit Price × (1 − Discount Percentage / 100)
```

Only orders with the following statuses are included:

```text
delivered
completed
```

This prevents cancelled or otherwise unsuccessful transactions from being treated as realized sales.

---

# 11. Business Analysis

## 11.1 Order Status Distribution

The first SQL analysis examines the distribution of orders across different statuses.

This provides a high-level view of the order lifecycle and can help identify unusual concentrations in statuses such as cancelled, returned, or pending.

The analysis is implemented in `queries.sql`.

---

## 11.2 Top 10 Customers by Sales

Customers are ranked based on total realized sales.

The analysis joins:

```text
customers
    ↓
orders
    ↓
order_items
```

and calculates post-discount sales at the order-item level.

The output identifies the customers generating the highest sales value.

### Business Use Case

This analysis can support:

* Key-account identification
* Customer prioritization
* Loyalty strategies
* Targeted promotions
* Customer segmentation

---

## 11.3 Top 3 Products per Category

Products are ranked independently within each category.

A SQL window function is used:

```sql
ROW_NUMBER() OVER (
    PARTITION BY category
    ORDER BY total_sales DESC
)
```

The top three products in each category are then selected.

### Business Use Case

This analysis can support:

* Product assortment decisions
* Category management
* Inventory prioritization
* Promotion planning
* Product performance monitoring

---

## 11.4 Order and Payment Status Inconsistencies

The analysis checks for potentially inconsistent combinations between order and payment status.

Examples include:

```text
Cancelled + Paid
Returned + Paid
Delivered + Failed
```

These combinations may indicate:

* Operational process issues
* Delayed status updates
* Refund-processing problems
* Payment reconciliation issues
* Data-quality inconsistencies

These records should be investigated further before being used in financial reporting.

---

## 11.5 Sales by Product Category

Sales are aggregated by product category to compare category-level performance.

This provides a high-level view of where sales are concentrated across the product portfolio.

### Business Use Case

Category-level sales analysis can support:

* Portfolio management
* Category prioritization
* Sales strategy
* Inventory planning
* Marketing allocation

---

# 12. Data Quality vs. Business Analysis

An important aspect of this project is the separation between data preparation and business analysis.

The workflow does not immediately calculate KPIs from raw data.

Instead:

```text
Raw Data
   ↓
Quality Assessment
   ↓
Cleaning
   ↓
Validation
   ↓
Database
   ↓
Business Analysis
```

This reduces the risk of producing misleading business insights from inconsistent transactional data.

---

# 13. Technical Implementation

The project uses Python and pandas for the ETL and data-quality workflow.

SQLite is used as the relational database layer.

SQL is then used for analytical queries.

### Python

Python is responsible for:

* Data ingestion
* Profiling
* Cleaning
* Transformation
* Validation
* Database creation
* Data loading

### SQL

SQL is responsible for:

* Relational joins
* Aggregation
* Ranking
* CTE-based transformations
* Window functions
* Business-rule analysis

---

# 14. Main Deliverables

The project produces the following artifacts:

| File              | Description                        |
| ----------------- | ---------------------------------- |
| `ETL_Pipeline.py` | Main ETL and data-quality workflow |
| `schema.sql`      | SQLite database schema             |
| `queries.sql`     | Analytical SQL queries             |
| `README.md`       | Project documentation              |
| `Report.md`       | Detailed analytical report         |
| `data.zip`        | Raw datasets                       |

---

# 15. Limitations

Several limitations should be considered when interpreting the analysis.

First, the project focuses primarily on descriptive and diagnostic analytics rather than predictive modeling.

Second, potential order/payment inconsistencies are identified but not automatically corrected because the appropriate business resolution would require additional operational information.

Third, missing dates are investigated but are not artificially imputed where doing so could introduce assumptions unsupported by the source data.

Finally, the analysis focuses on realized sales and does not currently include a complete profitability model involving product costs, operational costs, refunds, and other financial adjustments.

---

# 16. Potential Extensions

The current workflow provides a foundation for more advanced analysis.

Possible next steps include:

### Customer Analytics

* RFM segmentation
* Customer lifetime value
* Repeat purchase rate
* Customer retention
* Cohort analysis

### Product Analytics

* Product profitability
* Product contribution margin
* Category growth
* Product lifecycle analysis

### Operational Analytics

* Order fulfillment performance
* Cancellation rate
* Return rate
* Payment success rate
* Order processing time

### Data Engineering

* Automated ETL scheduling
* Incremental data loading
* Data-quality testing framework
* SQL Server implementation
* Production-grade data warehouse

### Business Intelligence

* Sales KPI dashboard
* Customer performance dashboard
* Product/category performance dashboard
* Payment and order reconciliation dashboard

---

# 17. Conclusion

This project demonstrates an end-to-end approach to transforming raw e-commerce data into a structured analytical environment.

Rather than focusing only on SQL queries or exploratory analysis, the workflow addresses the complete data lifecycle:

```text
Ingestion
→ Profiling
→ Data Quality
→ Cleaning
→ Validation
→ Relational Modeling
→ Data Loading
→ SQL Analysis
→ Business Interpretation
```

The project demonstrates practical capabilities across data analytics, SQL, ETL, relational database design, and data-quality management.

The resulting workflow provides a foundation that can be extended toward more advanced BI, analytics engineering, and data engineering use cases.
