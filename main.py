import os
import sys
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from models import Produto, ProdutoCreate, ProdutoUpdate
import database as db

# --- SETUP PARA WEBSOCKETS (NOTIFICAÇÕES PUSH) ---
from fastapi import WebSocket, WebSocketDisconnect

class NotificacaoManager:
    def __init__(self):
        self.conexoes_ativas: List[WebSocket] = []

    async def conectar(self, websocket: WebSocket):
        await websocket.accept()
        self.conexoes_ativas.append(websocket)

    def desconectar(self, websocket: WebSocket):
        if websocket in self.conexoes_ativas:
            self.conexoes_ativas.remove(websocket)

    async def enviar_para_todos(self, mensagem: dict):
        for conexao in self.conexoes_ativas:
            try:
                await conexao.send_json(mensagem)
            except Exception:
                pass

notificacoes_manager = NotificacaoManager()
# --------------------------------------------------

# Criação da instância da aplicação com metadados para o Swagger UI
app = FastAPI(
    title="API de Produtos - Exemplo Mobile",
    description=(
        "Web service simples em Python com FastAPI para estudantes de Desenvolvimento Mobile "
        "realizarem testes práticos de consumo de APIs REST (GET, POST, PUT, DELETE) com dados salvos em JSON."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração de CORS totalmente liberada para qualquer origem, método ou cabeçalho
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


def obter_caminho_static(nome_arquivo: str) -> str:
    """Localiza arquivos na pasta static considerando execução local, Render ou PyInstaller."""
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "static", nome_arquivo)


@app.get(
    "/",
    tags=["Geral"],
    summary="Página inicial da API",
    description="Retorna uma mensagem de boas-vindas e instrui onde acessar a documentação interativa e os tutoriais."
)
def raiz():
    return {
        "mensagem": "🚀 Bem-vindo à API de Exemplo para Desenvolvimento Mobile!",
        "documentacao": "/docs",
        "tutoriais": {
            "atividade_1_produtos_api": "/tutorial",
            "atividade_2_notificacoes_push": "/tutorial-notificacoes"
        },
        "endpoints": {
            "listar_produtos": "GET /produtos",
            "buscar_produto": "GET /produtos/{id}",
            "criar_produto": "POST /produtos",
            "atualizar_produto": "PUT /produtos/{id}",
            "remover_produto": "DELETE /produtos/{id}",
            "conectar_notificacoes": "WS /ws/notificacoes"
        }
    }


@app.get(
    "/tutorial",
    response_class=FileResponse,
    tags=["Documentação & Tutoriais"],
    summary="Atividade 1: Tutorial de Consumo de API (Catálogo de Produtos)",
    description="Apresenta o tutorial completo em HTML para criar o app Flutter que consome a API de produtos."
)
def obter_tutorial_produtos():
    caminho = obter_caminho_static("tutorial.html")
    if not os.path.exists(caminho):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento tutorial de produtos não encontrado no servidor."
        )
    return FileResponse(caminho, media_type="text/html; charset=utf-8")


@app.get(
    "/tutorial-notificacoes",
    response_class=FileResponse,
    tags=["Documentação & Tutoriais"],
    summary="Atividade 2: Tutorial de Notificações Push Simuladas (WebSockets)",
    description="Apresenta o tutorial completo em HTML para implementar notificações push com WebSockets no Flutter."
)
@app.get(
    "/tutorial/notificacoes",
    response_class=FileResponse,
    include_in_schema=False
)
def obter_tutorial_notificacoes():
    caminho = obter_caminho_static("tutorial_notificacoes.html")
    if not os.path.exists(caminho):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento tutorial de notificações não encontrado no servidor."
        )
    return FileResponse(caminho, media_type="text/html; charset=utf-8")




@app.get(
    "/produtos",
    response_model=List[Produto],
    tags=["Produtos"],
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


@app.get(
    "/produtos/{produto_id}",
    response_model=Produto,
    tags=["Produtos"],
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


@app.post(
    "/produtos",
    response_model=Produto,
    status_code=status.HTTP_201_CREATED,
    tags=["Produtos"],
    summary="Cadastrar novo produto",
    description="Cria um novo produto com ID sequencial automático e salva no arquivo JSON."
)
def criar_produto(novo_produto: ProdutoCreate):
    return db.criar_produto(novo_produto)


@app.put(
    "/produtos/{produto_id}",
    response_model=Produto,
    tags=["Produtos"],
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


@app.delete(
    "/produtos/{produto_id}",
    status_code=status.HTTP_200_OK,
    tags=["Produtos"],
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


# --- ENDPOINTS PARA SIMULAÇÃO DE NOTIFICAÇÕES PUSH ---
from pydantic import BaseModel

class NotificacaoPayload(BaseModel):
    titulo: str = "Aviso do Professor"
    mensagem: str = "Nova funcionalidade liberada!"

@app.websocket("/ws/notificacoes")
async def websocket_notificacoes(websocket: WebSocket):
    """
    Endpoint WebSocket para os apps dos alunos se conectarem.
    Fica aguardando mensagens enviadas pelo servidor.
    """
    await notificacoes_manager.conectar(websocket)
    try:
        while True:
            # O servidor fica ouvindo, caso o client mande algo, apenas ignoramos ou tratamos
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        notificacoes_manager.desconectar(websocket)

@app.post(
    "/notificacoes/enviar", 
    tags=["Notificações"], 
    summary="Disparar notificação para todos os apps conectados",
    description="Endpoint usado pelo professor para enviar um Push simulado para todo mundo."
)
async def disparar_notificacao_geral(payload: NotificacaoPayload):
    # Em pydantic v2 usamos model_dump, se der erro cai pro .dict()
    dados = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
    await notificacoes_manager.enviar_para_todos(dados)
    return {
        "sucesso": True, 
        "mensagem": f"Notificação disparada para {len(notificacoes_manager.conexoes_ativas)} dispositivos conectados!"
    }


def obter_ip_local() -> str:
    """Detecta o endereço IP local da máquina na rede Wi-Fi / Ethernet."""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    import uvicorn
    import os

    porta = int(os.environ.get("PORT", 8000))
    ip_local = obter_ip_local()

    print("\n" + "=" * 70)
    print("  🚀 SERVIDOR DA API DE PRODUTOS INICIADO COM SUCESSO!")
    print("=" * 70)
    print(f"  📖 Documentação Swagger UI:  http://localhost:{porta}/docs")
    print(f"  📖 Documentação ReDoc:       http://localhost:{porta}/redoc")
    print(f"  📘 Atividade 1 (Produtos):   http://localhost:{porta}/tutorial")
    print(f"  🔔 Atividade 2 (Push WSS):   http://localhost:{porta}/tutorial-notificacoes")
    print("-" * 70)
    print("  📲 Para Conectar seu App Mobile:")
    print(f"     • Emulador Android:        http://10.0.2.2:{porta}")
    print(f"     • Simulador iOS / Web:     http://localhost:{porta}")
    print(f"     • Aparelho Físico (Wi-Fi): http://{ip_local}:{porta}")
    print("-" * 70)
    print(f"  💾 Arquivo de Dados (JSON):  {db.DB_FILE}")
    print("  💡 Pressione CTRL + C para encerrar o servidor a qualquer momento.")
    print("=" * 70 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=porta, log_level="info")

