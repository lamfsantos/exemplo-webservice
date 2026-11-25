from fastapi import APIRouter
from schemas import HealthResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse, summary="Verificação de Saúde da API")
async def health_check():
    """
    Rota pública de verificação de integridade (Health Check).
    Utilizada pelo Render e monitores (UptimeRobot, cron-job) para evitar cold start.
    """
    return {"status": "ok"}
