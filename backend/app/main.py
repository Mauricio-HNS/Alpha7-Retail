from fastapi import FastAPI

app = FastAPI(
    title="Alpha7 Retail API",
    version="0.1.0",
    description="Compras, estoque e inteligência de reposição para varejo de moda."
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "alpha7-retail-api"}
