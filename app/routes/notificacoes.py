from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from bson import ObjectId
from app.db.database import notificacoes_collection
from app.schemas.notificacao_schema import NotificacaoBase, NotificacaoComID, StatusNotificacao
from datetime import datetime
import math

router = APIRouter()

@router.get("/notificacoes", response_model=List[NotificacaoComID])
async def listar_notificacoes(status: Optional[str] = Query(None)):
    filtro = {"status": status} if status else {}
    notificacoes = await notificacoes_collection.find(filtro).sort("data", -1).to_list(100)

    resultados = []

    for n in notificacoes:
        try:
            n["_id"] = str(n["_id"])
            
            # Corrigir campos obrigatórios
            if isinstance(n.get("transacao_id"), float) and math.isinf(n["transacao_id"]):
                n["transacao_id"] = "indefinido"
            elif n.get("transacao_id") is None:
                n["transacao_id"] = "indefinido"
            else:
                n["transacao_id"] = str(n["transacao_id"])

            if "conta_id" not in n or not isinstance(n["conta_id"], str):
                n["conta_id"] = "desconhecido"

            if "cliente_id" not in n or not isinstance(n["cliente_id"], int):
                n["cliente_id"] = -1  # valor default

            resultados.append(n)

        except Exception as e:
            print(f"⚠️ Erro ao preparar notificação: {e}")
            continue

    return resultados
# PUT /notificacoes/{id}
@router.put("/notificacoes/{notificacao_id}")
async def atualizar_status_notificacao(notificacao_id: str, novo_status: StatusNotificacao = Query(...)):
    try:
        resultado = await notificacoes_collection.update_one(
            {"_id": ObjectId(notificacao_id)},
            {"$set": {"status": novo_status.value, "data": datetime.utcnow()}}
        )
        if resultado.modified_count == 0:
            raise HTTPException(status_code=404, detail="Notificação não encontrada")
        return {"msg": "Status atualizado com sucesso"}
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

@router.get("/notificacoes/ultimas")
async def ultimas_notificacoes(qtd: int =5):
    notificacoes = await notificacoes_collection.find({}).sort("data", -1).limit(qtd).to_list(qtd)

    for n in notificacoes:
        n["_id"] = str(n["_id"])

    return notificacoes

# GET /notificacoes/resumo
@router.get("/notificacoes/resumo")
async def resumo_notificacoes():
    pipeline = [
        {
            "$group": {
                "_id": {
                    "status": "$status",
                    "nivel_risco": "$nivel_risco"
                },
                "total": {"$sum": 1}
            }
        }
    ]

    resultado = await notificacoes_collection.aggregate(pipeline).to_list(None)

    resumo = {
        "novo": 0,
        "em_analise": 0,
        "resolvido": 0,
        "baixo_risco": 0,
        "alto_risco": 0,
        "total": 0
    }

    for r in resultado:
        status = r["_id"]["status"]
        risco = r["_id"]["nivel_risco"]
        count = r["total"]

        resumo["total"] += count

        if status == "novo":
            resumo["novo"] += count
        elif status == "em_analise":
            resumo["em_analise"] += count
        elif status == "resolvido":
            resumo["resolvido"] += count

        if risco == "baixo":
            resumo["baixo_risco"] += count
        elif risco == "alto":
            resumo["alto_risco"] += count

    return resumo
