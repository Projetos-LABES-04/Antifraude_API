from fastapi import APIRouter, HTTPException,status
from app.db.database import db
from bson import ObjectId  # Para lidar com ObjectId
from app.schemas.transacao_schema import Transacao
from fastapi.responses import JSONResponse

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


@router.post(
    "/transacoes",
    response_model=Transacao,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova transação (só para testar validações)"
)
async def criar_transacao(transacao: Transacao):
    try:
        # Aqui você poderia inserir no banco:
        # result = await db["todo_collection"].insert_one(transacao.dict(exclude={"_id"}))
        # transacao._id = str(result.inserted_id)

        # Para fins de teste, só devolvemos o próprio objeto:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=transacao.dict()
        )
    except Exception as e:
        # Se algo der errado dentro da validação (raro, pois Pydantic já validou),
        # ou numa lógica extra, retornamos erro 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )