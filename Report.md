
# Sales Analysis Report

## Overview

This analysis covers a synthetic e-commerce dataset for 2024–2025. The data was cleaned using Python and loaded into SQLite for SQL-based analysis.

Sales were calculated at the order-item level as:

`quantity × unit_price × (1 - discount_percent / 100)`

Only successful orders with status `delivered` or `completed` were included in sales analysis. In the provided dataset, no `completed` orders were present, so the sales results are effectively based on `delivered` orders.

## Key Insights

### 1. Strong concentration of sales in Mobile & Accessories

The Mobile & Accessories category generated approximately **16.52 billion Toman** in sales, making it the largest category by a significant margin. The second-largest category, Fashion & Apparel, generated approximately **4.86 billion Toman**.

This indicates a strong concentration of sales in the Mobile & Accessories category and suggests that changes in demand, pricing, or availability in this category could have a significant impact on overall sales performance.

### 2. Significant order-payment inconsistencies

The analysis identified **563 potentially inconsistent order/payment combinations**:

- 284 cancelled orders with `partially_paid` payments
- 279 returned orders with `paid` payments

These cases may indicate issues in payment reconciliation, refund processing, or order-status synchronization. They should be reviewed as part of the financial and operational control process.

## Data Quality Notes

The raw data was checked for missing values, duplicate records, invalid values, data types, and referential integrity.

Key cleaning decisions included:

- Removing exact duplicate records from customers and order_items.
- Removing order-item records with missing or non-positive quantities.
- Removing order-item records with negative unit prices.
- Filling missing discount percentages with zero, assuming that a missing discount represents no discount.
- Replacing missing categorical values with `Unknown`.
- Keeping missing order and payment dates as NULL because their correct values could not be reliably inferred.
- Keeping negative order/payment amounts because they may represent refunds, adjustments, or other financial events.
- Deduplicating customer records by `customer_id` while keeping the first record when conflicting duplicate records could not be reliably resolved.

After cleaning, the dataset contained:

- 5,000 customers
- 300 products
- 30,000 orders
- 70,796 order items
- 30,000 payments
