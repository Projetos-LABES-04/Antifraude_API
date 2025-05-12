from fastapi import APIRouter
from schemas.transacao_schema import TransacaoBase
from schemas.notificacao_schema import NotificacaoBase
from db import db
from datetime import datetime

router = APIRouter()

@router.post("/verificar_transacao")
async def verificar_transacao(transacao: TransacaoBase):
    # Aqui você adaptaria o dado para o modelo de ML (FORMATAR AINDA)
    transacao_dict = transacao.dict()

    # Chamada ao seu modelo de ML (isso é só ilustrativo)(FORMATAR AINDA)
    resultado_ml = modelo.predict([transacao_dict])[0]

    # Se for fraude, criar uma notificação no MongoDB
    if resultado_ml == "fraude":
        notificacao = NotificacaoBase(
            transacao_id=transacao.transacao_id,
            conta_id=transacao.conta_id,
            cliente_id=transacao.cliente_id,
            mensagem="Transação suspeita detectada com alto risco.",
            nivel_risco="alto",  # você pode ajustar com base no score do modelo
            data=datetime.utcnow(),
        )
        await db["notificacoes"].insert_one(notificacao.dict())

    return {"resultado": resultado_ml}
