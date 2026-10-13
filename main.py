import os
import sys
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import database as db
from routers import (
    produtos_router,
    auth_router,
    notificacoes_router,
    formulario_router,
)

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

# =====================================================================
# INCLUSÃO DOS ROTEADORES MODULARES
# =====================================================================
app.include_router(produtos_router)
app.include_router(auth_router)
app.include_router(notificacoes_router)
app.include_router(formulario_router)


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
        "mensagem": "🚀 Bem-vindo à API de Exemplo para Desenvolvimento Mobile & Web!",
        "documentacao": "/docs",
        "tutoriais": {
            "atividade_1_produtos_api": "/tutorial",
            "atividade_2_notificacoes_push": "/tutorial-notificacoes",
            "web_1_teste_formulario": "/teste-formulario"
        },
        "endpoints": {
            "listar_produtos": "GET /produtos",
            "buscar_produto": "GET /produtos/{id}",
            "criar_produto": "POST /produtos",
            "atualizar_produto": "PUT /produtos/{id}",
            "remover_produto": "DELETE /produtos/{id}",
            "autenticacao_cadastro": "POST /auth/cadastrar",
            "autenticacao_login_json": "POST /auth/login",
            "autenticacao_token_oauth2": "POST /auth/token",
            "autenticacao_perfil": "GET /auth/me",
            "conectar_notificacoes": "WS /ws/notificacoes",
            "teste_formulario_html": "GET, POST /teste-formulario"
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
    print(f"  📝 Web 1 (Teste Form HTML):  http://localhost:{porta}/teste-formulario")
    print(f"  🔐 Autenticação JWT:       http://localhost:{porta}/auth/login (Swagger: /docs)")
    print("-" * 70)
    print("  📲 Para Conectar seu App Mobile:")
    print(f"     • Emulador Android:        http://10.0.2.2:{porta}")
    print(f"     • Simulador iOS / Web:     http://localhost:{porta}")
    print(f"     • Aparelho Físico (Wi-Fi): http://{ip_local}:{porta}")
    print("-" * 70)
    print(f"  💾 Banco de Produtos (JSON): {db.DB_FILE}")
    print(f"  💾 Banco de Usuários (JSON): {db.USUARIOS_FILE}")
    print("  💡 Pressione CTRL + C para encerrar o servidor a qualquer momento.")
    print("=" * 70 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=porta, log_level="info")
