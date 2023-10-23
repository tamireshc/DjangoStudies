from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.models.curso import Curso
from src.config.deps import get_session

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso: Curso, db: AsyncSession = Depends(get_session)):
    novo_curso = Curso(
        titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas
    )
    db.add(novo_curso)
    await db.commit()
    return novo_curso


@router.get("/", response_model=List[Curso])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(Curso)
        result = await db.execute(query)
        cursos: List[Curso] = result.scalars().all()
        return cursos


@router.get("/{id}", response_model=Curso)
async def get_curso(id: int, db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(Curso).filter(Curso.id == id)
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
    response_model=Curso,
    status_code=status.HTTP_202_ACCEPTED,
)
async def put_curso(
    id: int, curso: Curso, db: AsyncSession = Depends(get_session)
):
    async with db:
        query = select(Curso).filter(Curso.id == id)
        result = await db.execute(query)
        curso_att: Curso = result.scalar_one_or_none()

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
        query = select(Curso).filter(Curso.id == id)
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
