from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ProfileBase(BaseModel):
    perfil_nome: str = Field(..., max_length=100)


class ProfileCreate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    nome: str = Field(..., max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    senha: str = Field(..., min_length=8)
    profile: ProfileCreate


class UserUpdate(BaseModel):
    nome: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    profile: ProfileResponse

    model_config = ConfigDict(from_attributes=True)

