# Alpha7 Retail Backend

Backend da plataforma de compras e estoque inteligente para varejo de moda e lingerie.

## Objetivos da primeira versão

- Catálogo de produtos e SKUs
- Controle de estoque
- Histórico de vendas
- Fornecedores
- Recomendações de reposição
- Pedidos de compra
- Aprovação de compras
- Integração futura com Alpha7 AI

## Stack inicial

- Python 3.12+
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Pytest

A camada de domínio deve permanecer independente da IA. Cálculos financeiros e regras críticas são determinísticos; o agente Alpha7 será usado para análise, explicação e orquestração controlada.
