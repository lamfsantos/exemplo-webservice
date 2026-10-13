"""
Roteador para endpoints de Autenticação JWT.
Inclui rotas de cadastro (/auth/cadastrar), login via JSON (/auth/login),
login via formulário OAuth2 (/auth/token) e perfil autenticado (/auth/me).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import database as db
from auth import (
    autenticar_usuario,
    criar_access_token,
    gerar_hash_senha,
    obter_usuario_atual,
)
from models import LoginRequest, Token, Usuario, UsuarioCreate

auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])


@auth_router.post(
    "/cadastrar",
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo usuário",
    description="Cria um novo usuário na base de dados JSON com senha criptografada via bcrypt."
)
def cadastrar_usuario(novo_usuario: UsuarioCreate):
    existente = db.buscar_usuario_por_username(novo_usuario.username)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O nome de usuário '{novo_usuario.username}' já está em uso."
        )
        
    senha_hash = gerar_hash_senha(novo_usuario.senha)
    usuario_criado = db.criar_usuario(novo_usuario, senha_hash)
    return usuario_criado


@auth_router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login via JSON (Ideal para Apps Mobile & Web)",
    description="Recebe username e senha via corpo JSON e retorna o token de acesso Bearer JWT."
)
def login_json(credenciais: LoginRequest):
    usuario = autenticar_usuario(credenciais.username, credenciais.senha)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    token_jwt = criar_access_token(dados={"sub": usuario.username, "nome": usuario.nome or ""})
    return Token(access_token=token_jwt, token_type="bearer")


@auth_router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login OAuth2 via Formulário (Compatível com Swagger UI)",
    description="Endpoint OAuth2 padrão que recebe credenciais via form-urlencoded. Utilizado pelo botão 'Authorize' do Swagger."
)
def login_form_oauth2(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = autenticar_usuario(form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    token_jwt = criar_access_token(dados={"sub": usuario.username, "nome": usuario.nome or ""})
    return Token(access_token=token_jwt, token_type="bearer")


@auth_router.get(
    "/me",
    response_model=Usuario,
    status_code=status.HTTP_200_OK,
    summary="Consultar dados do usuário autenticado",
    description="Exemplo prático de endpoint protegido. Requer o envio do cabeçalho 'Authorization: Bearer <token>'."
)
def obter_meu_perfil(usuario_logado: Usuario = Depends(obter_usuario_atual)):
    """Retorna os dados cadastrais do usuário atualmente conectado."""
    return usuario_logado
