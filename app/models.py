from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import relationship

from .database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    perfil_nome = Column(String(100), nullable=False)

    user = relationship("User", back_populates="profile", uselist=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    senha = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False, unique=True)

    profile = relationship("Profile", back_populates="user", uselist=False)

    __table_args__ = (
        UniqueConstraint("profile_id", name="uq_users_profile_id"),
    )

