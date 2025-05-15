from fastapi import FastAPI
from app.routes.transacao import router as transacao_router
from app.routes import fraude


app = FastAPI()

# Registrar as rotas
app.include_router(transacao_router, tags=["Transações"])
app.include_router(fraude.router, tags=["Verificação de Fraude"])

# Rota para indicar que a API iniciou
@app.get("/")
async def root():
    return {"mensagem": "API Antifraude iniciada com sucesso!"} 
