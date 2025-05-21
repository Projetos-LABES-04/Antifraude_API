from pydantic import BaseModel

class LoginInput(BaseModel):
    matricula: int
    senha: str