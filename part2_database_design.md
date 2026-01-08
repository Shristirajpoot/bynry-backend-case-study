# Part 2: Database Design

## Requirements Recap
- Companies can have multiple warehouses
- Products can exist in multiple warehouses
- Inventory changes must be tracked
- Suppliers provide products
- Products can be bundles

---

## Schema Design

### Tables

Company  
- id (UUID, PK)  
- name (VARCHAR)

Warehouse  
- id (UUID, PK)  
- company_id (UUID, FK)  
- name (VARCHAR)  
- location (TEXT)

Product  
- id (UUID, PK)  
- name (VARCHAR)  
- sku (VARCHAR, UNIQUE)  
- price (DECIMAL)  
- product_type (STANDARD / BUNDLE)

Inventory  
- id (UUID, PK)  
- product_id (UUID, FK)  
- warehouse_id (UUID, FK)  
- quantity (INT)  
- UNIQUE(product_id, warehouse_id)

InventoryLog  
- id (UUID, PK)  
- inventory_id (UUID, FK)  
- change (INT)  
- reason (VARCHAR)  
- created_at (TIMESTAMP)

Supplier  
- id (UUID, PK)  
- name (VARCHAR)  
- contact_email (VARCHAR)

ProductSupplier  
- product_id (UUID, FK)  
- supplier_id (UUID, FK)

BundleItems  
- bundle_id (UUID, FK)  
- child_product_id (UUID, FK)  
- quantity (INT)

---

## Design Decisions
- Inventory separated from Product to support multiple warehouses
- InventoryLog added for auditability and compliance
- Unique constraints prevent duplicate inventory rows
- Indexes on SKU and foreign keys for performance
- BundleItems enables composite products

---

## Missing Requirements / Questions
1. Is SKU global or company-specific?
2. How are returns handled?
3. Should bundles auto-adjust child inventory?
4. How is “recent sales activity” defined?
5. Can products have multiple suppliers?
6. Are audit logs required for regulatory compliance?
