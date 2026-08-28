from fastapi import FastAPI
from app.api import crud_router, purchasing_router

app = FastAPI(
    title="Alpha7 Retail API",
    version="0.1.0",
    description="Compras, estoque e inteligência de reposição para varejo de moda."
)

app.include_router(crud_router)
app.include_router(purchasing_router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "alpha7-retail-api"}
