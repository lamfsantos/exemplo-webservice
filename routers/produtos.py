"""
Roteador para gerenciamento do catálogo de produtos.
Suporta operações REST completas: listar, buscar por ID, cadastrar, atualizar e remover.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

import database as db
from auth import obter_usuario_atual
from models import Produto, ProdutoCreate, ProdutoUpdate, Usuario

produtos_router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],
)


@produtos_router.get(
    "",
    response_model=List[Produto],
    summary="Listar todos os produtos",
    description="Retorna a lista completa de produtos cadastrados. Permite filtrar por disponibilidade ou termo de busca."
)
def listar_produtos(
    apenas_disponiveis: Optional[bool] = Query(None, description="Se true, lista apenas produtos disponíveis"),
    busca: Optional[str] = Query(None, description="Filtrar produtos por termo no nome ou descrição")
):
    produtos = db.listar_todos()
    
    if apenas_disponiveis is not None:
        produtos = [p for p in produtos if p.disponivel == apenas_disponiveis]
        
    if busca:
        termo = busca.lower()
        produtos = [
            p for p in produtos 
            if termo in p.nome.lower() or (p.descricao and termo in p.descricao.lower())
        ]
        
    return produtos


@produtos_router.get(
    "/{produto_id}",
    response_model=Produto,
    summary="Buscar produto por ID",
    description="Retorna os detalhes de um produto a partir de seu ID numérico."
)
def buscar_produto(produto_id: int):
    produto = db.buscar_por_id(produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado."
        )
    return produto


# =====================================================================
# DICA DIDÁTICA PARA PROTEGER ROTAS COM JWT EM AULA:
# Para exigir autenticação em qualquer endpoint abaixo (ex: POST, PUT, DELETE),
# basta adicionar a dependência 'usuario_logado: Usuario = Depends(obter_usuario_atual)'
# como parâmetro da função.
#
# Exemplo protegido:
# @produtos_router.post("", response_model=Produto, status_code=status.HTTP_201_CREATED)
# def criar_produto(novo_produto: ProdutoCreate, usuario_logado: Usuario = Depends(obter_usuario_atual)):
#     return db.criar_produto(novo_produto)
# =====================================================================

@produtos_router.post(
    "",
    response_model=Produto,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo produto",
    description="Cria um novo produto com ID sequencial automático e salva no arquivo JSON."
)
def criar_produto(novo_produto: ProdutoCreate):
    return db.criar_produto(novo_produto)


@produtos_router.put(
    "/{produto_id}",
    response_model=Produto,
    summary="Atualizar produto existente",
    description="Atualiza um ou mais campos de um produto existente. Campos omitidos permanecem inalterados."
)
def atualizar_produto(produto_id: int, dados: ProdutoUpdate):
    produto_atualizado = db.atualizar_produto(produto_id, dados)
    if not produto_atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado para atualização."
        )
    return produto_atualizado


@produtos_router.delete(
    "/{produto_id}",
    status_code=status.HTTP_200_OK,
    summary="Remover produto",
    description="Exclui um produto do arquivo JSON a partir do seu ID."
)
def remover_produto(produto_id: int):
    sucesso = db.remover_produto(produto_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado para exclusão."
        )
    return {
        "sucesso": True,
        "mensagem": f"Produto com ID {produto_id} removido com sucesso."
    }
