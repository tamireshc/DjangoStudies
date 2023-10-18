from fastapi import APIRouter, status, HTTPException, Path, Response, Header
from typing import List
from models import Curso, cursos

router = APIRouter()


@router.get(
    "/cursos",
    description="Exibe todos os cursos cadastrados",
    summary="Retorna todos os cursos",
    response_model=List[Curso],
)
async def get_cursos():
    return cursos


@router.get("/cursos/{id}")
async def get_curso(
    id: int = Path(
        title="Id do curso",
        description="valor de 1 a 2",
        gt=0,
        lt=3,
    )
):
    try:
        curso = cursos[id - 1]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado",
        )


@router.post("/cursos", status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso):
    cursos.routerend(curso)
    return curso


@router.put("/cursos/{id}")
async def put_curso(id: int, cursoReq: Curso):
    for curso in cursos:
        if id == curso.id:
            index = cursos.index(curso)
            cursos[index] = cursoReq
        return cursos[index]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não existe esse curso",
        )


@router.delete("/cursos/{id}")
async def delete_curso(id: int):
    for curso in cursos:
        if id == curso.id:
            index = cursos.index(curso)
            cursos.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado",
        )


@router.get("/calculadora")
async def calculadora(
    a: int,
    b: int,
    c: int,
    x: str = Header(
        default=None,
    ),
):
    result = a + b + c
    print(x)
    return {"soma": result}
