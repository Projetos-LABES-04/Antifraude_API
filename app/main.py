from fastapi import FastAPI
from app.routes.transacao import router as transacao_router


app = FastAPI()

# Registrar as rotas
app.include_router(transacao_router, tags=["Transações"])


@app.get("/")
async def root():
    return {"mensagem": "API Antifraude iniciada com sucesso!"} 
