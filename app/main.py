from fastapi import FastAPI
from app.api.transacao import router as transacao_router

app = FastAPI()

# Registrar as rotas
app.include_router(transacao_router, prefix="/api/v1/transacoes", tags=["Transações"])