from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post(
    "/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_usuario(
    usuario_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    try:
        usuario = crud.create_user(db, usuario_in)
    except crud.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso.",
        )
    return usuario


@router.get(
    "/",
    response_model=List[schemas.UserResponse],
)
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    usuarios = crud.get_users(db, skip=skip, limit=limit)
    return usuarios


@router.get(
    "/{usuario_id}",
    response_model=schemas.UserResponse,
)
def obter_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
):
    usuario = crud.get_user(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )
    return usuario


@router.put(
    "/{usuario_id}",
    response_model=schemas.UserResponse,
)
def atualizar_usuario(
    usuario_id: int,
    usuario_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
):
    try:
        usuario = crud.update_user(db, usuario_id, usuario_in)
    except crud.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso.",
        )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    return usuario


@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remover_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
):
    removido = crud.delete_user(db, usuario_id)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

