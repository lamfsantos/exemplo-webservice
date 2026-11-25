import os
from fastapi import FastAPI, Request, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from security import AuthError
from config import settings
from routers import health, auth, items, me

# Configuração do Rate Limiting (100 requisições por minuto por IP)
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(
    title="Desafio Mobile API - Catálogo de Obras & Avaliações",
    description="""
API RESTful desenvolvida para simular um teste técnico de desenvolvimento mobile.

### Funcionalidades:
* **Autenticação:** Login com credenciais de teste e emissão de Bearer JWT.
* **Catálogo de Obras:** Listagem com busca, paginação, filtro por categoria, status de favorito e nota média.
* **Avaliações (Reviews):** Envio e atualização de notas (1 a 5 estrelas) com comentários.
* **Favoritos:** Gerenciamento dos itens favoritos do usuário.

### Como testar no Swagger:
1. Faça login em `POST /auth/login` com as credenciais de teste fornecidas.
2. Copie o token retornado.
3. Clique no botão **Authorize** (topo direito) e cole o token.
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Registra o estado do limiter no app
app.state.limiter = limiter

# Middleware de CORS liberado para qualquer origem (Apps Mobile, Emuladores, Web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handler customizado para Rate Limit Exceeded
@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"error": "Muitas requisições. Limite de 100 requisições por minuto atingido."}
    )

# Handler para erros de autenticação customizados
@app.exception_handler(AuthError)
async def custom_auth_handler(request: Request, exc: AuthError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": exc.detail},
        headers={"WWW-Authenticate": "Bearer"}
    )

# Handler geral para exceções HTTP garantindo formato { "error": ... }
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    if isinstance(detail, dict) and "error" in detail:
        content = detail
    elif isinstance(detail, str):
        content = {"error": detail}
    else:
        content = {"error": detail}
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=exc.headers or {}
    )

# Redireciona a raiz para a documentação interativa (/docs)
@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/docs")

# Registro dos Routers na Raiz e no prefixo /api/v1 (compatibilidade total com o desafio)
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(health.router)
api_v1.include_router(auth.router)
api_v1.include_router(items.router)
api_v1.include_router(me.router)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(me.router)
app.include_router(api_v1)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", settings.PORT))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
