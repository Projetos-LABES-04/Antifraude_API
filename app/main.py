from fastapi import FastAPI
from app.routes.transacao import router as transacao_router
from app.routes import conta
from app.routes import dashboard

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta


app = FastAPI(debug=True)


app.include_router(conta.router)

# Configurações fixas
SECRET_KEY = "chave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Usuário fixo
FAKE_USER = {
    "username": "admin",
    "password": "123456"
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função para autenticar
def authenticate_user(username: str, password: str):
    return username == FAKE_USER["username"] and password == FAKE_USER["password"]

# Criar token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Rota para login
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Rota protegida
@app.get("/protegido")
async def rota_protegida(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username != FAKE_USER["username"]:
            raise HTTPException(status_code=401, detail="Usuário inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"mensagem": f"Bem-vindo, {username}!"}






app.include_router(dashboard.router)

# Registrar as rotas
app.include_router(transacao_router, tags=["Transações"])

# Rota para indicar que a API iniciou
@app.get("/")
async def root():
    return {"mensagem": "API Antifraude iniciada com sucesso!"}

