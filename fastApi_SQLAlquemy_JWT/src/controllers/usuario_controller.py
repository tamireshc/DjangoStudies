from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario import UsuarioModel
from schemas.usuario_schema import (
    UsuarioSchemaArtigos,
    UsuarioSchemaBase,
    UsuarioSchemaUpdate,
    UsuarioShcemaCreate,
)
from config.deps import get_session
from config.auth import get_current_user
from config.security import gerar_hash_senha
from config.auth import autenticar, criar_token_acesso

router = APIRouter()


@router.get("/logado", response_model=UsuarioSchemaBase)
def get_logao(usario_logado: UsuarioModel = Depends(get_current_user)):
    return usario_logado


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UsuarioSchemaBase,
)
async def post_usuario(
    usuario: UsuarioShcemaCreate, db: AsyncSession = Depends(get_session)
):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        eh_admin=usuario.eh_admin,
    )
    async with db:
        db.add(novo_usuario)
        await db.commit()
        return novo_usuario


@router.get("/", response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(UsuarioModel)
        result = await db.execute(query)
        usuarios = result.scalars().all()
        return usuarios


@router.get("/{id}", response_model=UsuarioSchemaArtigos)
async def get_usuario(id: int, db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(UsuarioModel).filter(UsuarioModel.id == id)
        result = await db.execute(query)
        usuario = result.scalars().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )


@router.put(
    "/{id}",
    response_model=UsuarioSchemaBase,
    status_code=status.HTTP_202_ACCEPTED,
)
async def put_usuario(
    id: int,
    usuario: UsuarioSchemaUpdate,
    db: AsyncSession = Depends(get_session),
):
    async with db:
        query = select(UsuarioModel).filter(UsuarioModel.id == id)
        result = await db.execute(query)
        usuario_att: UsuarioSchemaBase = result.scalars().one_or_none()

        if usuario_att:
            if usuario.nome:
                usuario_att.nome = usuario.nome
            if usuario.sobrenome:
                usuario_att.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_att.email = usuario.email
            if usuario.senha:
                usuario_att.senha = gerar_hash_senha(usuario.senha)
            if usuario.eh_admin:
                usuario_att.eh_admin = usuario.eh_admin

            await db.commit()
            return usuario_att

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id: int, db: AsyncSession = Depends(get_session)):
    async with db:
        query = select(UsuarioModel).filter(UsuarioModel.id == id)
        result = await db.execute(query)
        usuario = result.scalars().one_or_none()

        if usuario:
            await db.delete(usuario)
            await db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_logao),
):
    usuario = await autenticar(
        email=form_data.username, senha=form_data.password, db=db
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário ou senha incorretos",
        )
    return JSONResponse(
        content={
            "access_token": criar_token_acesso(sub=usuario.email),
            "token_type": "bearer",
        },
        status_code=status.HTTP_200_OK,
    )
