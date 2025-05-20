from pydantic import BaseModel

class LoginInput(BaseModel):
    matricula: str
    senha: str