from fastapi import FastAPI
from app.routes.usuario import router as usuario_router
from app.routes.transacao import router as transacao_router


app = FastAPI()

# Registrar as rotas
app.include_router(transacao_router, tags=["Transações"])
app.include_router(usuario_router, tags=["Usuários"])



# Rota para indicar que a API iniciou
@app.get("/")
async def root():
    return {"mensagem": "API Antifraude iniciada com sucesso!"}

