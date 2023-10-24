from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from src.models.curso import CursoModel


class AlunoModel(SQLModel, table=True):
    __tablename__: str = "alunos"
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    curso_id: int = Field(default=None, foreign_key="cursos.id")

    curso: CursoModel = Relationship()
