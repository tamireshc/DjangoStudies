from typing import Optional

from pydantic import BaseModel, validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @validator("titulo")
    def validar_titulo(cls, value: str):
        palavras = value.split()
        if len(palavras) < 3:
            raise ValueError("O título deve ter mais que 2 palavras")
        return value

    @validator("aulas")
    def validar_aulas(cls, value: int):
        aulas = value
        if aulas < 10:
            raise ValueError("O curso não pode ter menos que 10 aulas")


cursos = [
    Curso(id=1, titulo="Inicial 2, 3", aulas=112, horas=58),
    Curso(id=2, titulo="segunda 2, 3", aulas=12, horas=5),
]
