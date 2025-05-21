from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from bson import ObjectId
from app.db.database import notificacoes_collection
from app.schemas.notificacao_schema import NotificacaoBase, NotificacaoComID, StatusNotificacao
from datetime import datetime

router = APIRouter()

@router.get("/notificacoes", response_model=List[NotificacaoComID])
async def listar_notificacoes(status: Optional[str] = Query(None)):
    """
    Retorna todas as notificações, ordenadas por data decrescente.
    É possível filtrar por status: pendente, resolvida, visualizada...
    """
    filtro = {"status": status} if status else {}
    notificacoes = await notificacoes_collection.find(filtro).sort("data", -1).to_list(100)
    
    # Converte ObjectId para string
    for n in notificacoes:
        n["_id"] = str(n["_id"])
    return notificacoes

# ✅ PUT /notificacoes/{id}
@router.put("/notificacoes/{notificacao_id}")
async def atualizar_status_notificacao(notificacao_id: str, novo_status: StatusNotificacao = Query(...)):
    try:
        resultado = await notificacoes_collection.update_one(
            {"_id": ObjectId(notificacao_id)},
            {"$set": {"status": novo_status, "data": datetime.utcnow()}}
        )
        if resultado.modified_count == 0:
            raise HTTPException(status_code=404, detail="Notificação não encontrada")
        return {"msg": "Status atualizado com sucesso"}
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    # CONTINUAR MEXENDO NESSA PARTE PRA BAIXO

# 📊 GET /notificacoes/resumo
@router.get("/notificacoes/resumo")
async def resumo_notificacoes():
    pipeline = [
        {
            "$group": {
                "_id": {"status": "$status", "nivel_risco": "$nivel_risco"},
                "total": {"$sum": 1}
            }
        }
    ]

    resultado = await notificacoes_collection.aggregate(pipeline).to_list(None)

    resumo = {
        "pendente": 0,
        "concluida": 0,
        "baixo_risco": 0,
        "medio_risco": 0,
        "alto_risco": 0,
        "total": 0
    }

    for r in resultado:
        status = r["_id"]["status"]
        risco = r["_id"]["nivel_risco"]
        count = r["total"]

        resumo["total"] += count

        if status in resumo:
            resumo[status] += count

        if risco == "baixo":
            resumo["baixo_risco"] += count
        elif risco == "médio":
            resumo["medio_risco"] += count
        elif risco == "alto":
            resumo["alto_risco"] += count

    return resumo