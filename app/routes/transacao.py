from fastapi import APIRouter, HTTPException,status
from app.db.database import db
from bson import ObjectId  # Para lidar com ObjectId
from app.schemas.transacao_schema import TransacaoBase

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

@router.get("/debug")
async def debug_transacoes():
    count = await db["todo_collection"].count_documents({})
    return {"total_transacoes": count}


@router.get("/debug/conexao")
async def debug_conexao():
    print("Conectado ao banco:", db.name)
    colecoes = await db.list_collection_names()
    print("Coleções disponíveis:", colecoes)
    return {
        "mensagem": "Verifique o terminal/log do servidor para ver os prints."
    }

@router.post("/avaliar")
async def avaliar_transacao(transacao: TransacaoBase):
    # Aqui, os dados JÁ estão validados
    return {"dados": transacao}