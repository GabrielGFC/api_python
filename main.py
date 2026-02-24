from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from database import get_connection

app = FastAPI()


# =========================
# MODELOS
# =========================

# Modelo de entrada (Request Body)
class Usuario(BaseModel):
    nome: str
    email: EmailStr

class UsuarioModel(BaseModel):
    id: int
    nome: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

class UsuarioCreateResponse(BaseModel):
    mensagem: str
    user: UsuarioModel

class UsuarioList(BaseModel):
    mensagem: str
    users: List[UsuarioModel]

class UsuarioUpdateResponse(BaseModel):
    mensagem: str
    user: UsuarioModel


# =========================
# CREATE
# =========================
@app.post("/api/usuarios", response_model=UsuarioCreateResponse, status_code=201)
def criar_usuario(usuario: Usuario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        INSERT INTO users (nome, email, created_at, updated_at)
        VALUES (%s, %s, %s, %s)
    """

    now = datetime.now()

    cursor.execute(sql, (usuario.nome, usuario.email, now, now))
    conn.commit()

    usuario_id = cursor.lastrowid

    cursor.execute(
        "SELECT id, nome, email, created_at, updated_at FROM users WHERE id = %s",
        (usuario_id,)
    )

    novo_usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "mensagem": "Usuário cadastrado com sucesso",
        "user": novo_usuario
    }


# =========================
# READ - LISTAR
# =========================
@app.get("/api/usuarios", response_model=UsuarioList)
def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, nome, email, created_at, updated_at FROM users"
    )

    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "mensagem": "Usuários encontrados com sucesso",
        "users": usuarios
    }

# =========================
# UPDATE
# =========================
@app.put("/api/usuarios/{id}", response_model=UsuarioUpdateResponse)
def atualizar_usuario(id: int, dados: Usuario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    now = datetime.now()

    cursor.execute(
        """
        UPDATE users
        SET nome = %s,
            email = %s,
            updated_at = %s
        WHERE id = %s
        """,
        (dados.nome, dados.email, now, id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    cursor.execute(
        "SELECT id, nome, email, created_at, updated_at FROM users WHERE id = %s",
        (id,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "mensagem": "Usuário atualizado com sucesso",
        "user": usuario
    }


# =========================
# DELETE
# =========================
@app.delete("/api/usuarios/{id}")
def deletar_usuario(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    cursor.close()
    conn.close()

    return {"mensagem": "Usuário removido com sucesso"}