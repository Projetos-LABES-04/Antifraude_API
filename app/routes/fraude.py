from fastapi import APIRouter
from app.schemas.transacao_schema import TransacaoBase
from app.schemas.notificacao_schema import NotificacaoBase
from app.db.database import notificacoes_collection
from app.db.database import db
from datetime import datetime


router = APIRouter()

# 🔧 Simulação de modelo de ML (substitua isso pelo seu modelo real)
def modelo_ml_mock(transacao_dict):
    valor = transacao_dict["transacao_valor"]
    # Simulando score com base no valor
    score = min(valor / 5000, 1.0)  # quanto maior o valor, maior o risco
    resultado = "fraude" if score > 0.5 else "normal"
    return resultado, score

# 🚨 Endpoint de verificação de transação
@router.post("/verificar_transacao")
async def verificar_transacao(transacao: TransacaoBase):
    transacao_dict = transacao.dict()
    resultado_ml, score = modelo_ml_mock(transacao_dict)

    if resultado_ml == "fraude":
        # Definir nível de risco com base no score
        if score >= 0.85:
            nivel_risco = "alto"
        elif score >= 0.5:
            nivel_risco = "médio"
        else:
            nivel_risco = "baixo"

        notificacao = NotificacaoBase(
            transacao_id=transacao.transacao_id,
            conta_id=transacao.conta_id,
            cliente_id=transacao.cliente_id,
            mensagem="Transação suspeita detectada com comportamento anômalo.",
            nivel_risco=nivel_risco,
            status="pendente"
        )

        await notificacoes_collection.insert_one(notificacao.dict())

    return {
        "transacao_id": transacao.transacao_id,
        "resultado": resultado_ml,
        "score": round(score, 2)  # retorno útil pro front, inclusive
    }

