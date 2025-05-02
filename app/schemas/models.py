from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ID inválido do MongoDB")
        return str(v)  # Retorna como string para compatibilidade com JSON

class Transacao(BaseModel):
    _id: PyObjectId = Field(..., alias="_id")
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

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
