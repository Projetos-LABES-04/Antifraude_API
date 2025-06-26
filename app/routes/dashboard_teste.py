from fastapi import APIRouter, Query
from datetime import datetime
from typing import Optional
from app.db.database import db
from app.services.dashboard_service_teste import contar_transacoes_periodo

router = APIRouter()


@router.get("/dashboard/quantidade_transacoes")
async def quantidade_transacoes(
    periodo_inicio: Optional[datetime] = Query(None, description="Data inicial (ex: 2023-01-01)"),
    periodo_fim: Optional[datetime] = Query(None, description="Data final (ex: 2023-01-03)")
):
    return await contar_transacoes_periodo(periodo_inicio, periodo_fim)

@router.get("/notificacoes/quantidade")
async def contar_notificacoes():
    notificacoes = db["notificacoes"]
    quantidade = await notificacoes.count_documents({})
    return {"quantidade": quantidade}

@router.get("/dashboard/transacoes_suspeitas")
async def total_transacoes_suspeitas(
    data_inicio: datetime = Query(None),
    data_fim: datetime = Query(None)
):
    filtro = {"status": "suspeito"}

    if data_inicio and data_fim:
        # converte datetime -> string no mesmo formato armazenado
        data_inicio_str = data_inicio.strftime("%Y-%m-%d %H:%M:%S")
        data_fim_str = data_fim.strftime("%Y-%m-%d %H:%M:%S")
        filtro["transacao_data"] = {"$gte": data_inicio_str, "$lte": data_fim_str}

    total = await db["todo_collection"].count_documents(filtro)
    return {"total_suspeitas": total}

@router.get("/dashboard/valor_medio_suspeitas")
async def valor_medio_transacoes_suspeitas(
    data_inicio: datetime = Query(None),
    data_fim: datetime = Query(None)
):
    # Filtro base: transações suspeitas
    match_stage = {"status": "suspeito"}

    # Se houver filtro de datas, aplica o intervalo
    if data_inicio and data_fim:
        data_inicio_str = data_inicio.strftime("%Y-%m-%dT%H:%M:%S")
        data_fim_str = data_fim.strftime("%Y-%m-%dT%H:%M:%S")
        match_stage["transacao_data"] = {"$gte": data_inicio_str, "$lte": data_fim_str}

    # Pipeline de agregação: média do valor das transações suspeitas
    pipeline = [
        {"$match": match_stage},
        {
            "$group": {
                "_id": None,
                "valor_medio": {"$avg": "$transacao_valor"}
            }
        }
    ]

    resultado = await db["todo_collection"].aggregate(pipeline).to_list(length=1)

    # Retorna o valor médio ou 0.0 se não houver dados
    if resultado:
        return {"valor_medio": round(resultado[0]["valor_medio"], 2)}
    else:
        return {"valor_medio": 0.0}
    
@router.get("/dashboard/transacoes_analisadas")
async def total_transacoes_analisadas(
    data_inicio: datetime = Query(None),
    data_fim: datetime = Query(None)
):
    filtro = {"status": {"$exists": True}}

    if data_inicio and data_fim:
        data_inicio_str = data_inicio.strftime("%Y-%m-%dT%H:%M:%S")
        data_fim_str = data_fim.strftime("%Y-%m-%dT%H:%M:%S")
        filtro["transacao_data"] = {"$gte": data_inicio_str, "$lte": data_fim_str}

    total = await db["todo_collection"].count_documents(filtro)
    return {"total_analisadas": total}

@router.get("/dashboard/transacoes_nao_analisadas")
async def total_transacoes_nao_analisadas(
    data_inicio: datetime = Query(None),
    data_fim: datetime = Query(None)
):
    filtro = {"status": {"$exists": False}}

    if data_inicio and data_fim:
        data_inicio_str = data_inicio.strftime("%Y-%m-%dT%H:%M:%S")
        data_fim_str = data_fim.strftime("%Y-%m-%dT%H:%M:%S")
        filtro["transacao_data"] = {"$gte": data_inicio_str, "$lte": data_fim_str}

    total = await db["todo_collection"].count_documents(filtro)
    return {"total_nao_analisadas": total}