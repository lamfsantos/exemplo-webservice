import json
import os
import sys
from typing import List, Optional
from models import Produto, ProdutoCreate, ProdutoUpdate, Usuario, UsuarioCreate, UsuarioNoBanco

# Se compilado pelo PyInstaller (frozen), o caminho base é a pasta do .exe
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_FILE = os.path.join(DATA_DIR, "produtos.json")
USUARIOS_FILE = os.path.join(DATA_DIR, "usuarios.json")


# Usuários padrão criados caso o arquivo usuarios.json ainda não exista
# Senha de admin: admin123 | Senha de aluno: 123456
USUARIOS_PADRAO = [
    {
        "id": 1,
        "username": "admin",
        "nome": "Administrador",
        "senha_hash": "$2b$12$IGVyykEdqsuljV0dgRZsLucbV3Ycq4oyBOCZH6OPssh/J.WC4T2yC"
    },
    {
        "id": 2,
        "username": "aluno",
        "nome": "Aluno Exemplo",
        "senha_hash": "$2b$12$lwMkQGtdlgxjQn9hEmv8GeXgYJ33zN8p/HQiSNZrhOlSw1AGLMFiq"
    }
]

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


# =====================================================================
# OPERAÇÕES DE USUÁRIOS (PERSISTÊNCIA EM usuarios.json)
# =====================================================================

def carregar_usuarios() -> List[dict]:
    """Lê o arquivo usuarios.json e retorna a lista de usuários. Se não existir, cria com dados padrão."""
    if not os.path.exists(USUARIOS_FILE):
        salvar_usuarios(USUARIOS_PADRAO)
        return list(USUARIOS_PADRAO)
    
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                salvar_usuarios(USUARIOS_PADRAO)
                return list(USUARIOS_PADRAO)
            return json.loads(conteudo)
    except (json.JSONDecodeError, OSError):
        return list(USUARIOS_PADRAO)


def salvar_usuarios(usuarios: List[dict]) -> None:
    """Grava a lista de usuários no arquivo JSON com formatação legível."""
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)


def listar_usuarios() -> List[Usuario]:
    """Retorna todos os usuários cadastrados sem expor as senhas."""
    dados = carregar_usuarios()
    return [
        Usuario(id=u["id"], username=u["username"], nome=u.get("nome"))
        for u in dados
    ]


def buscar_usuario_por_username(username: str) -> Optional[UsuarioNoBanco]:
    """Busca um usuário pelo username exato (compara de forma case-insensitive)."""
    dados = carregar_usuarios()
    username_alvo = username.strip().lower()
    for u in dados:
        if u.get("username", "").strip().lower() == username_alvo:
            return UsuarioNoBanco(**u)
    return None


def buscar_usuario_por_id(usuario_id: int) -> Optional[Usuario]:
    """Busca um usuário pelo ID numérico sem expor a senha."""
    dados = carregar_usuarios()
    for u in dados:
        if u.get("id") == usuario_id:
            return Usuario(id=u["id"], username=u["username"], nome=u.get("nome"))
    return None


def criar_usuario(novo_usuario: UsuarioCreate, senha_hash: str) -> Usuario:
    """Gera um novo ID sequencial, adiciona o usuário com senha criptografada e persiste no JSON."""
    dados = carregar_usuarios()
    proximo_id = max([u.get("id", 0) for u in dados], default=0) + 1

    usuario_dict = {
        "id": proximo_id,
        "username": novo_usuario.username.strip(),
        "nome": novo_usuario.nome.strip() if novo_usuario.nome else None,
        "senha_hash": senha_hash
    }

    dados.append(usuario_dict)
    salvar_usuarios(dados)

    return Usuario(
        id=proximo_id,
        username=usuario_dict["username"],
        nome=usuario_dict["nome"]
    )
