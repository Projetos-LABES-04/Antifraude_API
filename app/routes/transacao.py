from fastapi import APIRouter, HTTPException,Query
from app.db.database import db
from bson import ObjectId  # Para lidar com ObjectId
from app.schemas.transacao_schema import TransacaoBase
from app.services.ml_client import chamar_servico_ml 
from time import sleep
import asyncio  # para pausa entre transações
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional

router = APIRouter()

# Função para converter ObjectId para string e corrigir valores inválidos
def serialize_document(document):
    document["_id"] = str(document["_id"])  # Converte ObjectId para string
    return document

@router.get("/transacoes")
async def listar_transacoes(
    limit:int = Query(50,ge=1,le=1000),
    skip:int = Query(0,ge=0),
    conta: Optional[str] = None,
    status: Optional[str] = None,
    valor_min: Optional[float] = None,
    valor_max: Optional[float] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
):


@router.post("/avaliar")
async def avaliar_transacao(transacao: TransacaoBase):
    return {"dados": transacao}


# Rota para processar transações pendentes em lotes
@router.post("/transacoes/processar_pendentes")
async def processar_em_lotes(
    lote: int = Query(1000, ge=100, le=2000),
    pausa: int = Query(2, ge=0, le=10, description="Pausa entre os lotes (segundos)"),
    entre_transacoes: float = Query(0.05, ge=0.0, le=1.0, description="Pausa entre cada requisição ao ML (segundos)")
):
   
    total_processadas = 0
    suspeitas = 0
    normais = 0
    lote_atual = 1

    while True:
        pendentes = await db["todo_collection"].find({"status": {"$exists": False}}).to_list(length=lote)
        if not pendentes:
            break

        print(f"🔄 Lote {lote_atual}: processando {len(pendentes)} transações...")

        for transacao in pendentes:
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

                total_processadas += 1
                if status == "suspeito":
                    suspeitas += 1
                else:
                    normais += 1

                if entre_transacoes > 0:
                    await asyncio.sleep(entre_transacoes)

            except Exception as e:
                print(f"⚠️ Erro ao processar transação {transacao.get('transacao_id')}: {e}")

        print(f"✅ Lote {lote_atual} finalizado. Total processadas: {total_processadas}")
        lote_atual += 1

        if pausa > 0:
            sleep(pausa)

    return JSONResponse(content={
        "msg": f"{total_processadas} transações processadas com sucesso",
        "lotes_processados": lote_atual - 1,
        "normais": normais,
        "suspeitas": suspeitas
    })