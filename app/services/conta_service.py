from typing import List, Optional
from app.schemas.conta_schema import Conta

# Simulando dados
contas_db = [
    Conta(id=1, nome="Conta 1", status="em análise"),
    Conta(id=2, nome="Conta 2", status="segura"),
    Conta(id=3, nome="Conta 3", status="em análise"),
    Conta(id=4, nome="Conta 4", status="segura"),
]

def listar_contas(status: Optional[str] = None) -> List[Conta]:
    if status:
        return [conta for conta in contas_db if conta.status == status]
    return contas_db
