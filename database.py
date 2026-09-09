import json
import os
import sys
from typing import List, Optional
from models import Produto, ProdutoCreate, ProdutoUpdate

# Se compilado pelo PyInstaller (frozen), o caminho base é a pasta do .exe
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FILE = os.path.join(BASE_DIR, "produtos.json")

DADOS_PADRAO = [
    {
        "id": 1,
        "nome": "Smartphone Galaxy A15",
        "preco": 1199.0,
        "descricao": "Tela 6.5 Super AMOLED, 128GB, 4GB RAM, Bateria 5000mAh",
        "disponivel": True
    },
    {
        "id": 2,
        "nome": "Fone de Ouvido Bluetooth JBL",
        "preco": 249.9,
        "descricao": "Cancelamento de ruído passivo, até 30h de bateria",
        "disponivel": True
    },
    {
        "id": 3,
        "nome": "Smartwatch Fit Pulse",
        "preco": 389.0,
        "descricao": "Monitor cardíaco, oxímetro, GPS integrado e resistência à água",
        "disponivel": False
    },
    {
        "id": 4,
        "nome": "Carregador Portátil Power Bank 20000mAh",
        "preco": 159.9,
        "descricao": "2 saídas USB-A e 1 USB-C Power Delivery 20W",
        "disponivel": True
    }
]


def carregar_produtos() -> List[dict]:
    """Lê o arquivo JSON e retorna a lista de produtos. Se o arquivo não existir, cria com dados padrão."""
    if not os.path.exists(DB_FILE):
        salvar_produtos(DADOS_PADRAO)
        return list(DADOS_PADRAO)
    
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                salvar_produtos(DADOS_PADRAO)
                return list(DADOS_PADRAO)
            return json.loads(conteudo)
    except (json.JSONDecodeError, OSError):
        return list(DADOS_PADRAO)


def salvar_produtos(produtos: List[dict]) -> None:
    """Grava a lista de produtos no arquivo JSON com formatação legível."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(produtos, f, indent=2, ensure_ascii=False)


def listar_todos() -> List[Produto]:
    """Retorna todos os produtos cadastrados."""
    dados = carregar_produtos()
    return [Produto(**p) for p in dados]


def buscar_por_id(produto_id: int) -> Optional[Produto]:
    """Busca um produto específico pelo seu ID."""
    dados = carregar_produtos()
    for item in dados:
        if item.get("id") == produto_id:
            return Produto(**item)
    return None


def criar_produto(novo_produto: ProdutoCreate) -> Produto:
    """Gera um novo ID sequencial, adiciona o produto e persiste no JSON."""
    dados = carregar_produtos()
    
    # Define o próximo ID (ou 1 se a lista estiver vazia)
    proximo_id = max([p.get("id", 0) for p in dados], default=0) + 1
    
    produto_dict = novo_produto.model_dump()
    produto_dict["id"] = proximo_id
    
    dados.append(produto_dict)
    salvar_produtos(dados)
    
    return Produto(**produto_dict)


def atualizar_produto(produto_id: int, dados_atualizacao: ProdutoUpdate) -> Optional[Produto]:
    """Atualiza apenas os campos enviados no JSON para o produto com o ID especificado."""
    dados = carregar_produtos()
    
    for i, item in enumerate(dados):
        if item.get("id") == produto_id:
            # Filtra apenas os campos enviados que não são None
            campos_atualizados = dados_atualizacao.model_dump(exclude_unset=True)
            dados[i].update(campos_atualizados)
            salvar_produtos(dados)
            return Produto(**dados[i])
            
    return None


def remover_produto(produto_id: int) -> bool:
    """Remove um produto pelo ID. Retorna True se removido, False se não encontrado."""
    dados = carregar_produtos()
    nova_lista = [p for p in dados if p.get("id") != produto_id]
    
    if len(nova_lista) == len(dados):
        return False
        
    salvar_produtos(nova_lista)
    return True
