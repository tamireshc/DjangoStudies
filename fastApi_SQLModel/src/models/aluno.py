from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Aluno(SQLModel, table=True):
    __tablename__: str = "alunos"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    curso_id: int = Field(default=None, foreign_key="curso.id")

    curso = Relationship()
