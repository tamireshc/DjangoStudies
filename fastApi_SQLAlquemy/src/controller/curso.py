from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schema import CursoSchema
from src.config.deps import get_session

router = APIRouter()

CS = CursoSchema
GS = get_session


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CS)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(GS)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)

    db.add(novo_curso)
    await db.commit()
    return novo_curso


@router.get("/", response_model=List[CursoSchema])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(CursoModel)
        result = await db.execute(query)
        cursos: List[CursoModel] = result.scalars().all()
        return cursos


@router.get("/{id}", response_model=CursoSchema)
async def get_curso(id: int, db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await db.execute(query)
        curso = result.scalar_one_or_none()
        if curso:
            return curso
        else:
            raise HTTPException(
                detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND
            )


@router.put("/{id}", response_model=CursoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_curso(
    id: int, curso: CursoSchema, db: AsyncSession = Depends(get_session)
):
    async with db:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await db.execute(query)
        curso_att = result.scalar_one_or_none()
        if curso_att:
            curso_att.titulo = curso.titulo
            curso_att.aulas = curso.aulas
            curso_att.horas = curso.horas
            await db.commit()
            return curso_att

        else:
            raise HTTPException(
                detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND
            )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id: int, db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await db.execute(query)
        curso_del = result.scalar_one_or_none()
        if curso_del:
            await db.delete(curso_del)
            await db.commit()
        else:
            raise HTTPException(
                detail="Curso não encontrado", status_code=status.HTTP_404_NOT_FOUND
            )
