from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.transacao import router as transacao_router
from app.routes import fraude
from app.routes.contas import router as contas_router
from app.routes import auth
from app.routes import notificacoes
from app.routes import contas
from app.routes.dashboard_teste import router as dashboard_teste

app = FastAPI(debug=True)

# CORS para liberar o acesso do front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://portal-de-analise-em-anomalias-tran-vert.vercel.app",
    "http://localhost:3000"],  # trocar origem quando hospedar front 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registrar as rotas
app.include_router(transacao_router, tags=["Transações"])
app.include_router(fraude.router, tags=["Verificação de Fraude"])
app.include_router(contas_router,tags=["Contas"])
app.include_router(notificacoes.router, tags=["Notificações"])
app.include_router(auth.router)
app.include_router(dashboard_teste, tags=["Dashboard Teste"])

@app.get("/")
async def root():
    return {"mensagem": "API Antifraude iniciada com sucesso!"} 
