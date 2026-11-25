from fastapi import APIRouter, HTTPException, status
from schemas import LoginRequest, LoginResponse, UserResponse, ErrorResponse
from database import supabase
from security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Credenciais inválidas"}
    },
    summary="Login de Aluno / Usuário"
)
async def login(credentials: LoginRequest):
    """
    Autentica o aluno/usuário através de e-mail e senha.
    Retorna o token JWT e os dados do usuário.
    """
    email_clean = credentials.email.strip().lower()
    try:
        response = supabase.table("users").select("*").eq("email", email_clean).execute()
        users = response.data or []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao consultar banco de dados: {str(e)}"
        )
    
    if not users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )
        
    user = users[0]
    if not verify_password(credentials.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos"
        )
        
    user_payload = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }
    
    token = create_access_token(user_payload)
    
    return {
        "token": token,
        "user": user_payload
    }
