from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Transacao(BaseModel):
    transacao_id: str
    cliente_id: int
    conta_id: str
    conta_destino_id: str
    mesma_titularidade: bool
    transacao_data: datetime
    transacao_valor: float
    transacao_tipo: str

    class Config:
        # Permitir que o Pydantic trabalhe com ObjectId do MongoDB
        json_encoders = {
            ObjectId: str  # Converter ObjectId para string
        }
