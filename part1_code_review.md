# Part 1: Code Review & Debugging

## Problem Overview
The original API endpoint for creating products compiles successfully but fails in production due to architectural and business logic issues.

---

## Issues Identified

### 1. No Transaction Safety
Product creation and inventory creation are committed in separate transactions.

**Impact:**  
If inventory creation fails, a product may exist without stock, leading to inconsistent data.

---

### 2. SKU Uniqueness Not Enforced
There is no validation to ensure SKU uniqueness.

**Impact:**  
Duplicate SKUs can break reporting systems and external integrations.

---

### 3. Incorrect Data Modeling
Product is directly linked to a warehouse, even though products can exist in multiple warehouses.

**Impact:**  
This design does not scale for multi-warehouse use cases.

---

### 4. Missing Input Validation
- Required fields are not validated
- Negative inventory quantities allowed
- Price handled as float

**Impact:**  
Leads to runtime errors, invalid data, and financial inaccuracies.

---

### 5. No Error Handling
Database failures are not handled gracefully.

**Impact:**  
Poor debugging experience and unreliable API behavior.

---

## Corrected Approach

### Key Fixes
- Use atomic transactions
- Enforce SKU uniqueness
- Separate Product and Inventory models
- Validate inputs
- Use decimal-safe pricing

---

## Corrected Code (Conceptual)

```python
with db.session.begin():
    if Product.query.filter_by(sku=data['sku']).first():
        return {"error": "SKU already exists"}, 409

    product = Product(
        name=data['name'],
        sku=data['sku'],
        price=Decimal(str(data['price']))
    )
    db.session.add(product)
    db.session.flush()

    inventory = Inventory(
        product_id=product.id,
        warehouse_id=data['warehouse_id'],
        quantity=data['initial_quantity']
    )
    db.session.add(inventory)
