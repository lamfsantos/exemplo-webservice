"""
Pacote de roteadores da aplicação FastAPI.
Exporta todos os roteadores modulares prontos para inclusão no main.py.
"""

from .produtos import produtos_router
from .auth import auth_router
from .notificacoes import notificacoes_router
from .formulario import formulario_router

__all__ = [
    "produtos_router",
    "auth_router",
    "notificacoes_router",
    "formulario_router",
]
