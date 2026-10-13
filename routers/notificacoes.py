"""
Roteador para suporte a WebSockets e simulação de Notificações Push.
Permite que aplicativos mobile (ex: Flutter) mantenham conexão WebSocket ativa
e recebam notificações em tempo real disparadas pelo professor via POST /notificacoes/enviar.
"""

from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel


class NotificacaoManager:
    """Gerencia conexões ativas via WebSocket para broadcast de notificações."""
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

notificacoes_router = APIRouter(tags=["Notificações"])


class NotificacaoPayload(BaseModel):
    """Payload de dados para envio de notificações simuladas."""
    titulo: str = "Aviso do Professor"
    mensagem: str = "Nova funcionalidade liberada!"


@notificacoes_router.websocket("/ws/notificacoes")
async def websocket_notificacoes(websocket: WebSocket):
    """
    Endpoint WebSocket para os apps dos alunos se conectarem.
    Fica aguardando mensagens enviadas pelo servidor em tempo real.
    """
    await notificacoes_manager.conectar(websocket)
    try:
        while True:
            # O servidor fica ouvindo; mensagens do cliente são recebidas e ignoradas
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        notificacoes_manager.desconectar(websocket)


@notificacoes_router.post(
    "/notificacoes/enviar",
    summary="Disparar notificação para todos os apps conectados",
    description="Endpoint usado pelo professor para enviar um Push simulado para todos os dispositivos conectados."
)
async def disparar_notificacao_geral(payload: NotificacaoPayload):
    dados = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
    await notificacoes_manager.enviar_para_todos(dados)
    return {
        "sucesso": True,
        "mensagem": f"Notificação disparada para {len(notificacoes_manager.conexoes_ativas)} dispositivos conectados!"
    }
