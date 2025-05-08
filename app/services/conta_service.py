from typing import List, Optional
from app.schemas.conta_schema import Conta

# Simulando dados
contas_db = [
    Conta(id=1, nome="transação 1", status="fraudulenta"),
    Conta(id=2, nome="transação 2", status="não fraudulenta"),
    Conta(id=3, nome="transação 3", status=""),
    Conta(id=4, nome="transação 4", status="segura"),
]

def listar_contas(status: Optional[str] = None) -> List[Conta]:
    if status:
        return [conta for conta in contas_db if conta.status == status]
    return contas_db
