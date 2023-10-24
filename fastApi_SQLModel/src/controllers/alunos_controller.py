from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config.deps import get_session
from src.models.aluno import AlunoModel

router = APIRouter()

GS = get_session


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AlunoModel)
async def post_aluno(aluno: AlunoModel, db: AsyncSession = Depends(GS)):
    novo_aluno = AlunoModel(name=aluno.name, curso_id=aluno.curso_id)

    db.add(novo_aluno)
    await db.commit()
    return novo_aluno


@router.get("/", response_model=List[AlunoModel])
async def get_alunos(db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(AlunoModel)
        result = await db.execute(query)
        alunos: List[AlunoModel] = result.scalars().all()
        return alunos


@router.get("/{id}", response_model=AlunoModel)
async def get_aluno(id: int, db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(AlunoModel).filter(AlunoModel.id == id)
        result = await db.execute(query)
        aluno = result.scalar_one_or_none()
        if aluno:
            return aluno
        else:
            raise HTTPException(
                detail="Aluno não encontrado",
                status_code=status.HTTP_404_NOT_FOUND,
            )


@router.put("/{id}", response_model=AlunoModel, status_code=status.HTTP_202_ACCEPTED)
async def put_aluno(
    id: int, aluno: AlunoModel, db: AsyncSession = Depends(get_session)
):
    async with db:
        query = select(AlunoModel).filter(AlunoModel.id == id)
        result = await db.execute(query)
        aluno_att = result.scalar_one_or_none()
        if aluno_att:
            aluno_att.name = aluno.name
            aluno_att.curso_id = aluno.curso_id
            await db.commit()
            return aluno_att

        else:
            raise HTTPException(
                detail="Aluno não encontrado",
                status_code=status.HTTP_404_NOT_FOUND,
            )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aluno(id: int, db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(AlunoModel).filter(AlunoModel.id == id)
        result = await db.execute(query)
        aluno_del = result.scalar_one_or_none()
        if aluno_del:
            await db.delete(aluno_del)
            await db.commit()
        else:
            raise HTTPException(
                detail="Aluno não encontrado",
                status_code=status.HTTP_404_NOT_FOUND,
            )
