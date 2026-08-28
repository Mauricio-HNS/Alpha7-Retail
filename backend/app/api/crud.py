from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Supplier, Product, Inventory, Sale
from app.schemas import SupplierCreate, SupplierRead, ProductCreate, ProductRead, InventoryRead, InventoryAdjust, SaleCreate, SaleRead

router = APIRouter(prefix="/api/v1", tags=["Retail"])

@router.post("/suppliers", response_model=SupplierRead, status_code=201)
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db)):
    obj = Supplier(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.get("/suppliers", response_model=list[SupplierRead])
def list_suppliers(db: Session = Depends(get_db)):
    return list(db.scalars(select(Supplier).order_by(Supplier.name)))

@router.get("/suppliers/{supplier_id}", response_model=SupplierRead)
def get_supplier(supplier_id: UUID, db: Session = Depends(get_db)):
    obj = db.get(Supplier, supplier_id)
    if not obj: raise HTTPException(404, "Fornecedor não encontrado")
    return obj

@router.post("/products", response_model=ProductRead, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    if not db.get(Supplier, data.supplier_id): raise HTTPException(400, "Fornecedor não encontrado")
    obj = Product(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj)
    inventory = Inventory(product_id=obj.id, quantity=0); db.add(inventory); db.commit()
    return obj

@router.get("/products", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return list(db.scalars(select(Product).order_by(Product.name)))

@router.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: UUID, db: Session = Depends(get_db)):
    obj = db.get(Product, product_id)
    if not obj: raise HTTPException(404, "Produto não encontrado")
    return obj

@router.get("/products/{product_id}/inventory", response_model=InventoryRead)
def get_inventory(product_id: UUID, db: Session = Depends(get_db)):
    obj = db.scalar(select(Inventory).where(Inventory.product_id == product_id))
    if not obj: raise HTTPException(404, "Estoque não encontrado")
    return obj

@router.put("/products/{product_id}/inventory", response_model=InventoryRead)
def adjust_inventory(product_id: UUID, data: InventoryAdjust, db: Session = Depends(get_db)):
    obj = db.scalar(select(Inventory).where(Inventory.product_id == product_id))
    if not obj: raise HTTPException(404, "Estoque não encontrado")
    obj.quantity = data.quantity; obj.reserved_quantity = data.reserved_quantity
    db.commit(); db.refresh(obj); return obj

@router.post("/sales", response_model=SaleRead, status_code=201)
def create_sale(data: SaleCreate, db: Session = Depends(get_db)):
    product = db.get(Product, data.product_id)
    if not product: raise HTTPException(404, "Produto não encontrado")
    inventory = db.scalar(select(Inventory).where(Inventory.product_id == data.product_id))
    if not inventory or inventory.quantity - inventory.reserved_quantity < data.quantity:
        raise HTTPException(409, "Estoque insuficiente")
    inventory.quantity -= data.quantity
    obj = Sale(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

@router.get("/sales", response_model=list[SaleRead])
def list_sales(db: Session = Depends(get_db)):
    return list(db.scalars(select(Sale).order_by(Sale.sold_at.desc())))
