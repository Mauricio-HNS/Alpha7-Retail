# Arquitetura Alpha7 Retail

## Camadas

- Frontend: React + TypeScript + Vite
- API: FastAPI
- Domínio: produtos, estoque, vendas, fornecedores e compras
- Persistência: PostgreSQL + SQLAlchemy
- Schema: Alembic
- Inteligência: motor determinístico de reposição; integração futura com Alpha7 AI

## Princípio

Regras financeiras e decisões críticas são determinísticas e auditáveis. A IA interpreta dados, explica recomendações e orquestra fluxos sujeitos a políticas e aprovação.

## Fluxo

Vendas + Estoque + Lead time + Estoque de segurança → Recomendação → Aprovação → Pedido → Auditoria
