from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TransacaoBase(BaseModel):
    transacao_id: str = Field(..., example="8c6a2055")
    cliente_id: int = Field(..., example=356)
    conta_id: str = Field(..., example="1cbe0f3f1")
    conta_destino_id: str = Field(..., example="10a4b8c06")
    mesma_titularidade: bool = Field(..., example=False)
    transacao_data: datetime = Field(..., example="2023-01-01T00:00:30")
    transacao_valor: float = Field(..., example=2474.5)
    transacao_tipo: str = Field(..., example="pix")

    class Config:
        from_attributes = True


class TransacaoDB(TransacaoBase):
    id: Optional[str] = Field(alias="_id")  # para mapear o ObjectId para string
