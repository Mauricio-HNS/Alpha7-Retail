"""Initial Alpha7 Retail schema."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("suppliers",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("name", sa.String(160), nullable=False),
        sa.Column("tax_id", sa.String(40), unique=True), sa.Column("email", sa.String(255)), sa.Column("phone", sa.String(40)),
        sa.Column("lead_time_days", sa.Integer(), nullable=False, server_default="7"), sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_index("ix_suppliers_name", "suppliers", ["name"])
    op.create_table("products",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("sku", sa.String(80), nullable=False), sa.Column("name", sa.String(200), nullable=False),
        sa.Column("category", sa.String(100), nullable=False), sa.Column("size", sa.String(30)), sa.Column("color", sa.String(50)),
        sa.Column("cost", sa.Numeric(12,2), nullable=False), sa.Column("price", sa.Numeric(12,2), nullable=False),
        sa.Column("minimum_stock", sa.Integer(), nullable=False, server_default="0"), sa.Column("safety_stock", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("supplier_id", sa.Uuid(), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.UniqueConstraint("supplier_id", "sku", name="uq_supplier_sku"))
    op.create_index("ix_products_sku", "products", ["sku"]); op.create_index("ix_products_name", "products", ["name"]); op.create_index("ix_products_supplier_id", "products", ["supplier_id"])
    op.create_table("inventory",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("product_id", sa.Uuid(), sa.ForeignKey("products.id"), nullable=False, unique=True),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="0"), sa.Column("reserved_quantity", sa.Integer(), nullable=False, server_default="0"), sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.create_table("sales",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("product_id", sa.Uuid(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False), sa.Column("unit_price", sa.Numeric(12,2), nullable=False), sa.Column("sold_at", sa.DateTime(), nullable=False))
    op.create_index("ix_sales_product_id", "sales", ["product_id"]); op.create_index("ix_sales_sold_at", "sales", ["sold_at"])
    op.create_table("purchase_orders",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("number", sa.String(40), nullable=False, unique=True), sa.Column("supplier_id", sa.Uuid(), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("status", sa.String(30), nullable=False), sa.Column("notes", sa.Text()), sa.Column("total", sa.Numeric(12,2), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("approved_at", sa.DateTime()))
    op.create_table("purchase_order_items",
        sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("purchase_order_id", sa.Uuid(), sa.ForeignKey("purchase_orders.id"), nullable=False),
        sa.Column("product_id", sa.Uuid(), sa.ForeignKey("products.id"), nullable=False), sa.Column("quantity", sa.Integer(), nullable=False), sa.Column("unit_cost", sa.Numeric(12,2), nullable=False))


def downgrade() -> None:
    op.drop_table("purchase_order_items"); op.drop_table("purchase_orders"); op.drop_index("ix_sales_sold_at", table_name="sales"); op.drop_index("ix_sales_product_id", table_name="sales"); op.drop_table("sales"); op.drop_table("inventory"); op.drop_index("ix_products_supplier_id", table_name="products"); op.drop_index("ix_products_name", table_name="products"); op.drop_index("ix_products_sku", table_name="products"); op.drop_table("products"); op.drop_index("ix_suppliers_name", table_name="suppliers"); op.drop_table("suppliers")
