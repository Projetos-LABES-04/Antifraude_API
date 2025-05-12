from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://labes:labes2025@cluster001.bohgn9f.mongodb.net/")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "todo_db")  # Nome do banco de dados padrão

# Criar o cliente MongoDB
client = AsyncIOMotorClient(MONGO_URI)

# Selecionar o banco de dados correto
db = client[MONGODB_DATABASE]

# Define a coleção que será usada
collection = db["todo_collection"]  # ← Substitua por seu nome real se for diferente