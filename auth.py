"""
Módulo de Autenticação com JWT (JSON Web Tokens) e Criptografia com BCrypt.

Projetado para ser didático e robusto para turmas de Desenvolvimento Mobile & Web.
Contém:
1. Funções de hash e verificação de senha com bcrypt.
2. Criação e decodificação de tokens JWT com expiração configurável.
3. Dependência `obter_usuario_atual` para proteger rotas existentes no FastAPI.
4. Endpoints de cadastro (/auth/cadastrar), login JSON (/auth/login),
   OAuth2 form (/auth/token para o Swagger) e rota de teste (/auth/me).
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import database as db
from models import LoginRequest, Token, Usuario, UsuarioCreate, UsuarioNoBanco

# =====================================================================
# CONFIGURAÇÕES DE SEGURANÇA E JWT
# =====================================================================

# Chave secreta usada para assinar digitalmente os tokens JWT
# Em produção, deve ser configurada via variável de ambiente JWT_SECRET_KEY
SECRET_KEY = os.environ.get(
    "JWT_SECRET_KEY", 
    "chave_secreta_super_segura_para_desenvolvimento_mobile_web"
)

# Algoritmo de criptografia do token (HS256 é o padrão recomendado pela indústria)
ALGORITHM = "HS256"

# Tempo de validade do token em minutos (padrão: 24 horas para facilitar testes práticos dos alunos)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))

# Esquema OAuth2 que lê o token enviado no cabeçalho 'Authorization: Bearer <token>'
# O tokenUrl aponta para /auth/token para integração automática com o cadeado do Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# =====================================================================
# FUNÇÕES DE CRIPTOGRAFIA DE SENHA (BCRYPT)
# =====================================================================

def gerar_hash_senha(senha: str) -> str:
    """Gera um hash seguro da senha em texto puro utilizando o algoritmo bcrypt."""
    senha_bytes = senha.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha_bytes, salt).decode("utf-8")


def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    """Valida se uma senha em texto puro corresponde ao hash bcrypt armazenado."""
    try:
        return bcrypt.checkpw(senha_pura.encode("utf-8"), senha_hash.encode("utf-8"))
    except Exception:
        return False


# =====================================================================
# FUNÇÕES DE TOKEN JWT
# =====================================================================

def criar_access_token(dados: dict, tempo_expiracao: Optional[timedelta] = None) -> str:
    """
    Gera um novo token JWT codificado com payload e data de expiração.
    Recebe um dicionário com claims (ex: {"sub": "aluno"}).
    """
    payload = dados.copy()
    
    agora = datetime.now(timezone.utc)
    if tempo_expiracao:
        expira_em = agora + tempo_expiracao
    else:
        expira_em = agora + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    payload.update({
        "exp": expira_em,
        "iat": agora
    })
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decodificar_token(token: str) -> dict:
    """
    Decodifica e valida a assinatura e expiração de um token JWT.
    Lança jwt.PyJWTError se o token for inválido ou estiver expirado.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# =====================================================================
# SERVIÇO DE AUTENTICAÇÃO E DEPENDÊNCIA DE PROTEÇÃO DE ROTAS
# =====================================================================

def autenticar_usuario(username: str, senha: str) -> Optional[UsuarioNoBanco]:
    """Busca o usuário no banco de dados e valida se a senha fornecida confere."""
    usuario = db.buscar_usuario_por_username(username)
    if not usuario:
        return None
    if not verificar_senha(senha, usuario.senha_hash):
        return None
    return usuario


async def obter_usuario_atual(token: str = Depends(oauth2_scheme)) -> Usuario:
    """
    Dependência do FastAPI para proteger rotas.
    
    Extrai o token JWT do cabeçalho 'Authorization: Bearer <token>', valida a
    assinatura/expiração e obtém o usuário no arquivo de dados.
    
    COMO PROTEGER QUALQUER ROTA NO SEU CÓDIGO (EXEMPLO PARA AULA):
    --------------------------------------------------------------
    from auth import obter_usuario_atual
    from models import Usuario
    
    @app.post("/produtos")
    def criar_produto(novo: ProdutoCreate, usuario: Usuario = Depends(obter_usuario_atual)):
        print(f"Produto sendo criado por: {usuario.username}")
        ...
    """
    credenciais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decodificar_token(token)
        username: Optional[str] = payload.get("sub")
        if not username:
            raise credenciais_exception
    except jwt.PyJWTError:
        raise credenciais_exception
        
    usuario = db.buscar_usuario_por_username(username)
    if usuario is None:
        raise credenciais_exception
        
    return Usuario(
        id=usuario.id,
        username=usuario.username,
        nome=usuario.nome
    )


# =====================================================================
# ROTEADOR DE AUTENTICAÇÃO (/auth)
# Disponibilizado aqui também para conveniência e compatibilidade retroativa
# =====================================================================

from routers.auth import auth_router  # noqa: E402, F401

