from fastapi import FastAPI
from app.routes import dashboard

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta


app = FastAPI(debug=True)


#app.include_router(conta.router)




app.include_router(dashboard.router)

# Registrar as rotas
#app.include_router(transacao_router, tags=["Transações"])

# Rota para indicar que a API iniciou
@app.get("/")
async def root():
    return {"mensagem": "API Antifraude iniciada com sucesso!"}

