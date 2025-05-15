from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.transacao import router as transacao_router


app = FastAPI()

# CORS para liberar o acesso do front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ou "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registrar as rotas
app.include_router(transacao_router, tags=["Transações"])

# Rota para indicar que a API iniciou
@app.get("/")
async def root():
    return {"mensagem": "API Antifraude iniciada com sucesso!"}

