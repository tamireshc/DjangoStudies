from sqlalchemy.ext.declarative import declarative_base


class Settigns(BaseException):
    """Configurações gerais da aplicação"""

    API_V1_STR: str = "/api/v1"
    # usuario acesso banco:senha  banco/ servidor : porta/ banco de dados
    DB_URl: str = "postgresql+asyncpg://root:1234567@localhost:5432/faculdade"
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True


settings = Settigns()
