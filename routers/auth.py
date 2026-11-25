from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    LoginRequest,
    RegisterRequest,
    AuthResponse,
    UserResponse,
    ErrorResponse
)
from database import supabase
from security import verify_password, hash_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Dados inválidos"},
        409: {"model": ErrorResponse, "description": "E-mail já cadastrado"}
    },
    summary="Cadastro de Novo Aluno / Usuário"
)
async def register(data: RegisterRequest):
    """
    Cadastra um novo aluno/usuário na plataforma.
    Gera o hash da senha e já retorna imediatamente o token JWT pronto para uso no app.
    """
    email_clean = data.email.strip().lower()
    name_clean = data.name.strip()

    # Verifica se e-mail já existe
    try:
        existing = supabase.table("users").select("id").eq("email", email_clean).execute()
        if existing.data:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado no sistema"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar e-mail: {str(e)}"
        )

    # Cria o hash da senha e insere o novo usuário
    password_hashed = hash_password(data.password)
    try:
        insert_res = supabase.table("users").insert({
            "name": name_clean,
            "email": email_clean,
            "password_hash": password_hashed
        }).execute()

        if not insert_res.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao salvar usuário no banco de dados"
            )
        new_user = insert_res.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao cadastrar usuário: {str(e)}"
        )

    user_payload = {
        "id": new_user["id"],
        "name": new_user["name"],
        "email": new_user["email"]
    }

    token = create_access_token(user_payload)

    return {
        "token": token,
        "user": user_payload
    }

@router.post(
    "/login",
    response_model=AuthResponse,
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

@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Não autorizado ou token expirado"}
    },
    summary="Perfil do Usuário Autenticado (Validação de Auto-Login)"
)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado a partir do token Bearer.
    Utilizado no app para checagem de auto-login na tela inicial (Splash).
    """
    return {
        "id": current_user["id"],
        "name": current_user.get("name", ""),
        "email": current_user["email"]
    }
