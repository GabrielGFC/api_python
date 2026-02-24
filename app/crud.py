from typing import List, Optional

from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from . import models, schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class EmailAlreadyExistsError(Exception):
    pass


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return (
        db.query(models.User)
        .options(joinedload(models.User.profile))
        .filter(models.User.id == user_id)
        .first()
    )


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return (
        db.query(models.User)
        .options(joinedload(models.User.profile))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise EmailAlreadyExistsError()

    profile = models.Profile(perfil_nome=user_in.profile.perfil_nome)
    hashed_password = get_password_hash(user_in.senha)

    user = models.User(
        nome=user_in.nome,
        email=user_in.email,
        senha=hashed_password,
        profile=profile,
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise EmailAlreadyExistsError() from exc

    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate) -> Optional[models.User]:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None

    if user_in.email and user_in.email != user.email:
        existing = get_user_by_email(db, user_in.email)
        if existing and existing.id != user.id:
            raise EmailAlreadyExistsError()

    if user_in.nome is not None:
        user.nome = user_in.nome
    if user_in.email is not None:
        user.email = user_in.email

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise EmailAlreadyExistsError() from exc

    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return False

    profile = user.profile

    db.delete(user)
    if profile:
        db.delete(profile)

    db.commit()
    return True

