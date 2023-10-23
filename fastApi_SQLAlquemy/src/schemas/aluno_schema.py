from typing import Optional

from pydantic import BaseModel


class AlunoSchema(BaseModel):
    id: Optional[int] = None
    name: str
    curso_id: int

    class Config:
        orm_mode = True
