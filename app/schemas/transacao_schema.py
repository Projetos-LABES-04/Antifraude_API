from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class Transacao(BaseModel):
    id: str = Field(..., alias="_id", example="680fe24ca2db5716d502f3ec")  # Usando alias
    transacao_id: str = Field(..., example="8c6a2055")
    cliente_id: int = Field(..., gt=0, example=356)
    conta_id: str = Field(..., example="1cbe0f3f1")
    conta_destino_id: str = Field(..., example="10a4b8c06")
    mesma_titularidade: bool = Field(..., example=False)
    transacao_data: datetime = Field(..., example="2023-01-01T00:00:30")
    transacao_valor: float = Field(..., gt=0, example=2474.5)
    transacao_tipo: Literal["pix", "boleto", "cartao", "transferencia"] = Field(..., example="pix")

    class Config:
        # Configurar o Pydantic para aceitar alias
        allow_population_by_field_name = True
