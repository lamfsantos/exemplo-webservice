from pydantic import BaseModel, Field
from typing import Optional


class ProdutoBase(BaseModel):
    """Modelo base com os atributos comuns de um Produto."""
    nome: str = Field(..., example="Smartphone Android Pro", description="Nome do produto")
    preco: float = Field(..., gt=0, example=1899.90, description="Preço unitário do produto (deve ser maior que zero)")
    descricao: Optional[str] = Field(None, example="Tela 6.5 polegadas, 128GB de armazenamento", description="Descrição detalhada do produto")
    disponivel: bool = Field(True, example=True, description="Indica se o produto está disponível em estoque")


class ProdutoCreate(ProdutoBase):
    """Modelo utilizado na criação de um novo produto (POST)."""
    pass


class ProdutoUpdate(BaseModel):
    """Modelo utilizado na atualização parcial ou total de um produto (PUT)."""
    nome: Optional[str] = Field(None, example="Smartphone Android Pro Atualizado")
    preco: Optional[float] = Field(None, gt=0, example=1799.90)
    descricao: Optional[str] = Field(None, example="Nova descrição do produto")
    disponivel: Optional[bool] = Field(None, example=False)


class Produto(ProdutoBase):
    """Modelo completo do produto retornado pela API (inclui o ID)."""
    id: int = Field(..., example=1, description="Identificador único do produto")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nome": "Smartphone Android Pro",
                "preco": 1899.90,
                "descricao": "Tela 6.5 polegadas, 128GB de armazenamento",
                "disponivel": True
            }
        }


# =====================================================================
# MODELOS DE USUÁRIO E AUTENTICAÇÃO JWT
# =====================================================================

class UsuarioBase(BaseModel):
    """Modelo base para usuário com campos comuns."""
    username: str = Field(..., example="aluno", description="Nome de usuário para login")
    nome: Optional[str] = Field(None, example="João da Silva", description="Nome completo do usuário")


class UsuarioCreate(UsuarioBase):
    """Modelo utilizado para o cadastro de novo usuário (POST /auth/cadastrar)."""
    senha: str = Field(..., min_length=4, example="123456", description="Senha de acesso (mínimo 4 caracteres)")


class Usuario(UsuarioBase):
    """Modelo público do usuário retornado pela API (sem senha)."""
    id: int = Field(..., example=1, description="Identificador único do usuário")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "aluno",
                "nome": "João da Silva"
            }
        }


class UsuarioNoBanco(Usuario):
    """Modelo interno do usuário com o hash da senha armazenado no JSON."""
    senha_hash: str = Field(..., description="Hash criptografado da senha com bcrypt")


class LoginRequest(BaseModel):
    """Modelo para login via corpo JSON (POST /auth/login), ideal para apps Mobile e Web."""
    username: str = Field(..., example="aluno", description="Nome de usuário")
    senha: str = Field(..., example="123456", description="Senha de acesso")


class Token(BaseModel):
    """Modelo de resposta contendo o token de acesso JWT retornado no login."""
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", description="Token de acesso JWT")
    token_type: str = Field("bearer", example="bearer", description="Tipo do token (sempre 'bearer')")


class TokenData(BaseModel):
    """Dados decodificados do payload do token JWT."""
    username: Optional[str] = None

