from fastapi import APIRouter
from app.schemas.transacao_schema import TransacaoBase
from app.schemas.notificacao_schema import NotificacaoBase
from app.db.database import notificacoes_collection
from app.db.database import db
from datetime import datetime


router = APIRouter()

# 🔧 Simulação de modelo de ML (substitua isso pelo seu modelo real)
def modelo_ml_mock(transacao_dict):
    # Exemplo: retorna "fraude" se valor for maior que 2500
    return "fraude" if transacao_dict["transacao_valor"] > 2500 else "normal"

# 🚨 Endpoint de verificação de transação
@router.post("/verificar_transacao")
async def verificar_transacao(transacao: TransacaoBase):
    transacao_dict = transacao.dict()

    # 🔍 Chamada ao modelo de machine learning (aqui simulado)
    resultado_ml = modelo_ml_mock(transacao_dict)

    # 🚨 Se for fraude, cria notificação automaticamente
    if resultado_ml == "fraude":
        notificacao = NotificacaoBase(
            transacao_id=transacao.transacao_id,
            conta_id=transacao.conta_id,
            cliente_id=transacao.cliente_id,
            mensagem="Transação suspeita detectada com comportamento anômalo.",
            nivel_risco="alto",  # você pode ajustar com base no score
            data=datetime.utcnow(),
            status="pendente"
        )
        await notificacoes_collection.insert_one(notificacao.dict())

    return {
        "transacao_id": transacao.transacao_id,
        "resultado": resultado_ml
    }
