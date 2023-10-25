from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


from src.config.config import settings


class ArtigoModel(settings.DBBaseModel):
    __tablename__ = "artigos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(256))
    url_fonte = Column(String(256))
    usuario_ir = Column(Integer, ForeignKey)
