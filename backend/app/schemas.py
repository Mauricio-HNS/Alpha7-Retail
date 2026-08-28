from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class SupplierBase(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    tax_id: str | None = None
    email: str | None = None
    phone: str | None = None
    lead_time_days: int = Field(default=7, ge=0)
    active: bool = True
class SupplierCreate(SupplierBase): pass
class SupplierRead(SupplierBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class ProductBase(BaseModel):
    sku: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=2, max_length=200)
    category: str = Field(min_length=2, max_length=100)
    size: str | None = None
    color: str | None = None
    cost: Decimal = Field(ge=0)
    price: Decimal = Field(ge=0)
    minimum_stock: int = Field(default=0, ge=0)
    safety_stock: int = Field(default=0, ge=0)
    supplier_id: UUID
    active: bool = True
class ProductCreate(ProductBase): pass
class ProductRead(ProductBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class InventoryRead(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int
    reserved_quantity: int
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class InventoryAdjust(BaseModel):
    quantity: int = Field(ge=0)
    reserved_quantity: int = Field(default=0, ge=0)

class SaleCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0)
    sold_at: datetime
class SaleRead(SaleCreate):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
