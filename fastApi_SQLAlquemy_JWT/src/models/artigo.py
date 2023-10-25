from sqlalchemy import Column, ForeignKey, Integer, String

# from sqlalchemy.orm import Base as DBBaseModel
from sqlalchemy.orm import relationship

from config.config import settings


class ArtigoModel(settings.DBBaseModel):
    __tablename__ = "artigos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(256))
    url_fonte = Column(String(256))
    descricao = Column(String(256))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship(
        "UsuarioModel", back_populates="artigos", lazy="joined"
    )
