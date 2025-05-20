from fastapi import APIRouter , HTTPException
from app.db.database import db
from app.schemas.conta_schema import ContaResumo

router = APIRouter()

@router.get("/contas/gestao",response_model=list[ContaResumo])
async def listar_resumo_contas():
    pipeline = [
        { "$sort": { "transacao_data": -1 } },
        {
            "$group": {
                "_id": "$conta_id",
                "cliente_id": { "$first": "$cliente_id" },
                "ultima_atividade": { "$first": "$transacao_data" },
                "valor_ultima": { "$first": "$transacao_valor" }
                # Não usamos status aqui pois ele ainda não existe
            }
        },
        {
            "$project": {
                "_id": 0,
                "conta_id": "$_id",
                "cliente_id": 1,
                "ultima_atividade": 1,
                "valor_ultima": 1,
                "status": { "$literal": "em_analise" }
            }
        }
    ]

    resultados = await db["todo_collection"].aggregate(pipeline).to_list(length=None)
    return resultados