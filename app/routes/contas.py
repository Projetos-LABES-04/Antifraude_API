from fastapi import APIRouter , HTTPException
from app.db.database import db
from app.schemas.conta_schema import ContaResumo
from datetime import datetime,timedelta

router = APIRouter()

@router.get("/contas/analise",response_model=list[ContaResumo])
async def listar_resumo_contas():
    try:
        data_limite = datetime.utcnow() - timedelta(days=90)

        pipeline = [
            { "$match": { "transacao_data": { "$gte": data_limite } } },
            { "$sort": { "transacao_data": -1 } },
            {
                "$group": {
                    "_id": "$conta_id",
                    "cliente_id": { "$first": "$cliente_id" },
                    "ultima_atividade": { "$first": "$transacao_data" },
                    "valor_ultima": { "$first": "$transacao_valor" }
                }
            },
            {
                "$project": {
                    "conta_id": "$_id",
                    "cliente_id": 1,
                    "ultima_atividade": 1,
                    "valor_ultima": 1,
                    "status": { "$literal": "análise" }
                }
            }
        ]

        resultado = await db["todo_collection"].aggregate(pipeline).to_list(length=None)
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))