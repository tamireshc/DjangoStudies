from sqlalchemy import Column, Integer, String

from src.config import settings


class CursoModel(settings.DBBaseModel):
    __tablename__ = "cursos"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    titulo: str = Column(String(100))
    aulas: int = Column(Integer)
    horas: int = Column(Integer)
