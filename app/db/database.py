from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
#load_dotenv()
from pathlib import Path

dotenv_path = Path(__file__).resolve().parents[2] / '.env'
print(f"🔍 Carregando .env de: {dotenv_path}")
load_dotenv(dotenv_path)

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://labes:labes2025@cluster001.bohgn9f.mongodb.net/")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE","todo_db")

print("⚠️ Debug - Testando variáveis:")
print(f"MONGO_URI -> {MONGO_URI}")
print(f"MONGODB_DATABASE -> {MONGODB_DATABASE}")


if not MONGO_URI:
    raise RuntimeError(" MONGO_URI não carregado!")

if not MONGODB_DATABASE:
    raise RuntimeError(" MONGODB_DATABASE não carregado!")



# Criar o cliente MongoDB
client = AsyncIOMotorClient(MONGO_URI)

# Selecionar o banco de dados correto
db = client[MONGODB_DATABASE]


if not MONGODB_DATABASE:
    raise ValueError("Environment variable 'MONGODB_DATABASE' is not set or is empty.")

print(f"MONGO_URI carregado: {MONGO_URI}")
print(f"MONGODB_DATABASE carregado: {MONGODB_DATABASE}")
