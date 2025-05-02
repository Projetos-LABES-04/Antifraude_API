from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class Transacao(BaseModel):
    transacao_id: str = Field(..., min_length=1)
    cliente_id: int
    conta_id: str
    conta_destino_id: str
    mesma_titularidade: bool
    transacao_data: datetime
    transacao_valor: float = Field(..., gt=0)
    transacao_tipo: str

    @validator("transacao_tipo")
    def validar_tipo_transacao(cls, v):
        tipos_validos = {"pix", "boleto", "ted", "doc", "transferencia"}
        if v.lower() not in tipos_validos:
            raise ValueError(f"Tipo de transação inválido: {v}")
        return v.lower()
