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
