from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NotificacaoBase(BaseModel):
    transacao_id: str = Field(..., example="8c6a2055")
    conta_id: str = Field(..., example="1cbe0f3f1")
    cliente_id: int = Field(..., example=356)
    data: datetime = Field(default_factory=datetime.utcnow)
    mensagem: str = Field(..., example="Transação suspeita detectada.")
    status: str = Field(default="pendente", example="pendente")
    nivel_risco: str = Field(default="alto", example="alto")

