from pydantic import BaseModel, Field
from typing import Literal
from uuid import UUID
from datetime import datetime

class Transacao(BaseModel):
    _id: str  # ID gerado pelo MongoDB (não precisa de validação adicional)
    transacao_id: str  # Um identificador único para a transação
    cliente_id: int  # ID do cliente envolvido
    conta_id: str  # Conta do cliente que fez a transação
    conta_destino_id: str  # Conta de destino da transação
    mesma_titularidade: bool  # Se a transação é entre contas do mesmo titular
    transacao_data: datetime  # Data e hora da transação
    transacao_valor: float = Field(gt=0, description="O valor da transação deve ser maior que zero.")  # Validando que o valor é positivo
    transacao_tipo: Literal["pix", "boleto", "cartao", "transferencia"]  # Tipos de transação permitidos

    class Config:
        # Garantir que o UUID seja convertido para string e que as datas sejam formatadas corretamente
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat(),
        }
