from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class StatusNotificacao(str, Enum):
    pendente = "pendente"
    concluida = "concluida"

class NotificacaoBase(BaseModel):
    transacao_id: str = Field(..., example="8c6a2055")
    conta_id: str = Field(..., example="1cbe0f3f1")
    cliente_id: int = Field(..., example=356)
    data: datetime = Field(default_factory=datetime.utcnow)
    mensagem: str = Field(..., example="Transação suspeita detectada.")
    status: StatusNotificacao = Field(default=StatusNotificacao.pendente)
    nivel_risco: str = Field(default="alto", example="alto")

    # 🔹 Saída: resposta incluindo o _id
class NotificacaoComID(NotificacaoBase):
    id: str = Field(..., alias="_id")  # ⬅️ Pega o _id do Mongo

