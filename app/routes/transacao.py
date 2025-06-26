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
from dateutil.parser import parse
import math


router = APIRouter()

# Função para converter ObjectId para string e corrigir valores inválidos
def serialize_document(document):
    document["_id"] = str(document["_id"])
    for key, value in document.items():
        if isinstance(value, float) and (
            value == float("inf") or
            value == float("-inf") or
            value != value  # NaN
        ):
            document[key] = None
    return document

@router.get("/transacoes")
async def listar_transacoes(
    limit: int = Query(50, ge=1, le=1000),
    skip: int = Query(0, ge=0),
    conta: Optional[str] = None,
    status: Optional[str] = None,
    valor_min: Optional[float] = None,
    valor_max: Optional[float] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
):
    try:
        filtro = {}
        if conta:
            filtro["conta_id"] = conta
        if status:
            if status =="análise":
                filtro["status"] = {"$exists":False}
            else:
                filtro["status"] = status
        if valor_min is not None or valor_max is not None:
            filtro["transacao_valor"] = {}
            if valor_min is not None:
                filtro["transacao_valor"]["$gte"] = valor_min
            if valor_max is not None:
                filtro["transacao_valor"]["$lte"] = valor_max
        if data_inicio and data_fim:
            try:
                inicio = parse(data_inicio)
                fim = parse(data_fim)
                filtro["transacao_data"] = {"$gte": inicio, "$lte": fim}
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Erro ao converter datas: {str(e)}")

        total = await db["todo_collection"].count_documents(filtro)
        transacoes = await db["todo_collection"].find(filtro).skip(skip).limit(limit).to_list(length=limit)
        
        print("Filtro aplicado:", filtro)
        return {
            "total": total,
            "dados": [serialize_document(t) for t in transacoes]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar transações: {str(e)}")


@router.post("/avaliar")
async def avaliar_transacao(transacao: TransacaoBase):
    return {"dados": transacao}

def corrigir_valores(transacao):
    """Corrige campos inválidos com valores padrão razoáveis."""
    campos_default = {
        "transacao_valor": 0.0,
        "transacao_data": "2023-01-01 00:00:00",
        "transacao_tipo": "pix",
        "cliente_id": -1,
        "conta_id": "desconhecido",
        "conta_destino_id": "desconhecido",
        "mesma_titularidade": False,
    }

    for campo, default in campos_default.items():
        valor = transacao.get(campo)

        if isinstance(valor, str) and valor.lower() in ["inf", "nan", ""]:
            transacao[campo] = default
        elif isinstance(valor, float) and (math.isinf(valor) or math.isnan(valor)):
            transacao[campo] = default
        elif valor is None:
            transacao[campo] = default

    return transacao

@router.post("/transacoes/processar_pendentes")
async def processar_em_lotes(
    lote: int = Query(100, ge=100, le=2000),
    entre_transacoes: float = Query(0.01, ge=0.0, le=1.0)
):
    total_processadas = 0
    suspeitas = 0
    normais = 0

    CAMPOS_OBRIGATORIOS = {
        "transacao_id", "cliente_id", "conta_id", "conta_destino_id",
        "mesma_titularidade", "transacao_data", "transacao_valor", "transacao_tipo"
    }

    pendentes = await db["todo_collection"].find({"status": {"$exists": False}}).to_list(length=lote)
    print(f"🔄 Processando {len(pendentes)} transações...")

    for transacao in pendentes:
        try:
            transacao["_id"] = str(transacao["_id"])

            if not CAMPOS_OBRIGATORIOS.issubset(transacao):
                print(f"⚠️ Transação {transacao.get('transacao_id')} ignorada: campos ausentes.")
                continue

            transacao = corrigir_valores(transacao)

            print(f"✅ Transação {transacao['transacao_id']} será processada pelo modelo")

            resultado = await chamar_servico_ml(transacao)
            status = "suspeito" if resultado["decisao_final"] == 1 else "normal"

            await db["todo_collection"].update_one(
                {"_id": ObjectId(transacao["_id"])},
                {"$set": {
                    "status": status,
                    "fraude_binario": resultado["decisao_final"],
                    "nivel_suspeita": resultado.get("nivel_suspeita"),
                    "motivo_alerta": resultado.get("motivo_alerta")
                }}
            )

            total_processadas += 1
            if status == "suspeito":
                suspeitas += 1
                if resultado.get("nivel_suspeita") in ["media", "alta"]:
                    await db["notificacoes"].insert_one({
                        "transacao_id": transacao["transacao_id"],
                        "mensagem": f"Transação suspeita detectada na conta {transacao['conta_id']}",
                        "nivel_risco": resultado.get("nivel_suspeita"),
                        "status": "novo",
                        "data": datetime.utcnow()
                    })
            else:
                normais += 1

            if entre_transacoes > 0:
                await asyncio.sleep(entre_transacoes)

        except Exception as e:
            print(f"⚠️ Erro ao processar transação {transacao.get('transacao_id')}: {e}")

    print(f"✅ Lote finalizado. Total processadas: {total_processadas}")

    return JSONResponse(content={
        "msg": f"{total_processadas} transações processadas com sucesso",
        "normais": normais,
        "suspeitas": suspeitas
    })