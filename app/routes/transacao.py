from fastapi import APIRouter, HTTPException
from app.db.database import db
from bson import ObjectId  # Para lidar com ObjectId
from app.schemas.transacao_schema import Transacao

router = APIRouter()

# Função para converter ObjectId para string e corrigir valores inválidos
def serialize_document(document):
    document["_id"] = str(document["_id"])
    for key, value in document.items():
        if isinstance(value, float) and (value == float("inf") or value == float("-inf") or value != value):  # Verifica NaN, inf e -inf
            document[key] = None  # Substitui valores inválidos por None
    return document

@router.get("/transacoes")
async def listar_transacoes():
    try:
        # Consultar todas as transações na coleção "todo_collection"
        transacoes = await db["todo_collection"].find().to_list(100)  # Limite de 100 documentos

        # Serializar os documentos para corrigir valores inválidos
        transacoes_serializadas = [serialize_document(doc) for doc in transacoes]

        return transacoes_serializadas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")
    

@router.post("/nova_transacao/")
async def criar_transacao(transacao: Transacao):
    try:
        # Os dados em 'transacao' já foram validados pelo Pydantic
        transacao_dict = transacao.dict()
        result = await db["todo_collection"].insert_one(transacao_dict)
        nova_transacao = await db["todo_collection"].find_one({"_id": result.inserted_id})
        return serialize_document(nova_transacao)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir a transação: {str(e)}")