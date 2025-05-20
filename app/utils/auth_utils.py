from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta


SECRET_KEY = "chave_muito_segura"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60

#Esse objeto vai cuidar de gerar e verificar hashes de senhas com segurança.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#gerar_hash_senha
def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

#Compara a senha digitada (senha_plana) com o hash armazenado (senha_hash)
def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_plana, senha_hash)

def gerar_token(dados: dict) -> str:
    to_encode = dados.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
