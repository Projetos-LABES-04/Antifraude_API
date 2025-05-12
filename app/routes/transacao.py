from fastapi import APIRouter, HTTPException,status
from app.db.database import db
from bson import ObjectId  # Para lidar com ObjectId
from app.schemas.transacao_schema import TransacaoBase
from app.services.ml_client import chamar_servico_ml 

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


@router.post("/avaliar")
async def avaliar_transacao(transacao: TransacaoBase):
    # Aqui, os dados JÁ estão validados
    return {"dados": transacao}


@router.post("/transacoes/processar_pendentes")
async def processar_transacoes_sem_status():
    """
    Processa todas as transações sem status.
    Envia para o modelo ML e atualiza o banco com o resultado.
    """
    try:
        transacoes_pendentes = await db["todo_collection"].find({"status": {"$exists": False}}).to_list(length=None)

        total = 0
        suspeitas = 0
        normais = 0

        for transacao in transacoes_pendentes:
            try:
                resultado = await chamar_servico_ml(transacao)
                status = "suspeito" if resultado == 1 else "normal"

                await db["todo_collection"].update_one(
                    {"_id": transacao["_id"]},
                    {"$set": {
                        "status": status,
                        "fraude_binario": resultado
                    }}
                )

                total += 1
                if status == "suspeito":
                    suspeitas += 1
                else:
                    normais += 1

            except Exception as e:
                print(f"Erro ao processar transação {transacao.get('transacao_id')}: {e}")

        return {
            "msg": f"{total} transações processadas com sucesso",
            "normais": normais,
            "suspeitas": suspeitas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar transações: {str(e)}")