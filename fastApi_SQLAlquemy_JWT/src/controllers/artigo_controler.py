from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from config.auth import get_current_user
from config.deps import get_session
from models.artigo import ArtigoModel
from models.usuario import UsuarioModel
from schemas.artigo_schema import ArtigoSchema

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(
    artigo: ArtigoSchema,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    print(usuario_logado)
    novo_artigo = ArtigoModel(
        titulo=artigo.titulo,
        descricao=artigo.descricao,
        url_fonte=artigo.url_fonte,
        usuario_id=usuario_logado.id,
    )

    db.add(novo_artigo)
    await db.commit()

    return novo_artigo


@router.get("/", response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(ArtigoModel)
        result = await db.execute(query)
        artigos: List[ArtigoModel] = result.unique().scalars().all()

        return artigos


@router.get("/{id}", response_model=ArtigoSchema)
async def get_artigo(id: int, db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(ArtigoModel).filter(ArtigoModel.id == id)
        result = await db.execute(query)
        artigo: ArtigoModel = result.unique().scalars().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo náo encontrado",
            )


@router.put("/{id}", response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_artigo(
    id: int,
    artigo: ArtigoSchema,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    async with db:
        query = select(ArtigoModel).filter(ArtigoModel.id == id)
        result = await db.execute(query)
        artigo_att: ArtigoModel = result.unique().scalars().one_or_none()

        if artigo_att:
            if artigo_att.titulo:
                artigo_att.titulo = artigo.titulo
            if artigo_att.descricao:
                artigo_att.descricao = artigo.descricao
            if artigo_att.url_fonte:
                artigo_att.url_fonte = artigo.url_fonte
            if usuario_logado.id != artigo_att.usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuário não tem permissão para atualizar o artigo",
                )

            await db.commit()
            return artigo_att

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo náo encontrado",
            )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(
    id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    async with db:
        query = select(ArtigoModel).filter(ArtigoModel.id == id)
        result = await db.execute(query)
        artigo: ArtigoModel = result.unique().scalars().one_or_none()

        if artigo:
            if usuario_logado.id == artigo.usuario_id:
                await db.delete(artigo)
                await db.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuário não tem permissão para deletar o artigo",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artigo não encontrado",
            )
