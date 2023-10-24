from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.config.deps import get_session
from src.models.curso import CursoModel

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
    db.add(novo_curso)
    await db.commit()
    return novo_curso


@router.get("/")
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(CursoModel)
        result = await db.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
    return cursos


@router.get("/{id}", response_model=CursoModel)
async def get_curso(id: int, db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await db.execute(query)
        curso = result.scalar_one_or_none()

    if curso:
        return curso
    else:
        raise HTTPException(
            detail="Curso não encontrado",
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.put(
    "/{id}",
    response_model=CursoModel,
    status_code=status.HTTP_202_ACCEPTED,
)
async def put_curso(
    id: int, curso: CursoModel, db: AsyncSession = Depends(get_session)
):
    async with db:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await db.execute(query)
        curso_att: CursoModel = result.scalar_one_or_none()

        if curso_att:
            curso_att.titulo = curso.titulo
            curso_att.aulas = curso.aulas
            curso_att.horas = curso.horas
            await db.commit()
            return curso_att
        else:
            raise HTTPException(
                detail="Curso não encontrado",
                status_code=status.HTTP_404_NOT_FOUND,
            )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id: int, db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await db.execute(query)
        curso = result.scalar_one_or_none()

    if curso:
        await db.delete(curso)
        await db.commit()
    else:
        raise HTTPException(
            detail="Curso não encontrado",
            status_code=status.HTTP_404_NOT_FOUND,
        )
