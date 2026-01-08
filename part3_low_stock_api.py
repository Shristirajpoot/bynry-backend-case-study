from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from sqlalchemy import func

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/api/companies/<company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    """
    Returns low-stock alerts for a company across all warehouses.
    """

    alerts = []

    inventories = (
        db.session.query(Inventory, Product, Warehouse, Supplier)
        .join(Product)
        .join(Warehouse)
        .join(ProductSupplier)
        .join(Supplier)
        .filter(Warehouse.company_id == company_id)
        .all()
    )

    for inventory, product, warehouse, supplier in inventories:

        recent_sales = (
            db.session.query(func.sum(Sales.quantity))
            .filter(
                Sales.product_id == product.id,
                Sales.warehouse_id == warehouse.id,
                Sales.created_at >= datetime.utcnow() - timedelta(days=30)
            )
            .scalar() or 0
        )

        if recent_sales == 0:
            continue

        avg_daily_sales = recent_sales / 30
        days_until_stockout = int(inventory.quantity / avg_daily_sales)

        if inventory.quantity <= product.low_stock_threshold:
            alerts.append({
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "warehouse_id": warehouse.id,
                "warehouse_name": warehouse.name,
                "current_stock": inventory.quantity,
                "threshold": product.low_stock_threshold,
                "days_until_stockout": days_until_stockout,
                "supplier": {
                    "id": supplier.id,
                    "name": supplier.name,
                    "contact_email": supplier.contact_email
                }
            })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })
