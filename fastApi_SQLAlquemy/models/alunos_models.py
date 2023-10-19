from sqlalchemy import Column, ForeignKey, Integer, String

from core.config import settings


class AlunosModel(settings.DBBaseModel):
    __tablename__ = "alunos"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String)
    curso_id = Column(Integer, ForeignKey("cursos.id"))
