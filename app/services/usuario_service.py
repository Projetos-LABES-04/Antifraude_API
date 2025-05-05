from app.db.database import usuario_collection
from typing import Optional, Dict, Any
from bson import ObjectId
from datetime import datetime
from passlib.context import CryptContext
from fastapi import HTTPException, status

class UsuarioService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def autenticar_usuario(self, nome: str, senha: str) -> Optional[Dict[str, Any]]:
        usuario = await usuario_collection.find_one({"nome": nome})
        
        if not usuario or not self.verificar_senha(senha, usuario["senha_hash"]):
            return None
            
        return {
            "id": str(usuario["_id"]),
            "nome": usuario["nome"],
            "criado_em": usuario["criado_em"]
        }

    async def criar_usuario(self, nome: str, senha: str) -> Dict[str, Any]:
        if await usuario_collection.find_one({"nome": nome}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já existe"
            )
            
        usuario_data = {
            "nome": nome,
            "senha_hash": self.hash_senha(senha),
            "criado_em": datetime.utcnow()
        }
        
        result = await usuario_collection.insert_one(usuario_data)
        return {
            "id": str(result.inserted_id),
            "nome": nome,
            "mensagem": "Usuário criado com sucesso"
        }

    def hash_senha(self, senha: str) -> str:
        return self.pwd_context.hash(senha)
        
    def verificar_senha(self, senha_plana: str, senha_hash: str) -> bool:
        return self.pwd_context.verify(senha_plana, senha_hash)

# Instância global assíncrona
usuario_service = UsuarioService()