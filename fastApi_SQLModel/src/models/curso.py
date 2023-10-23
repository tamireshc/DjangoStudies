from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel
from models.aluno import Aluno


class Curso(SQLModel, table=True):
    __tablename__: str = "cursos"
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    aulas: int
    horas: int

    aulas: List["Aluno"] = Relationship()
