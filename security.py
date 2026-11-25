import datetime
from typing import Optional, Dict, Any
import bcrypt
import jwt
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings

bearer_scheme = HTTPBearer(auto_error=False)

class AuthError(HTTPException):
    def __init__(self, message: str = "Token inválido ou expirado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )

def hash_password(password: str) -> str:
    """Gera hash seguro da senha com salt usando bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto puro bate com o hash bcrypt."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False

def create_access_token(user_data: Dict[str, Any], expires_delta: Optional[datetime.timedelta] = None) -> str:
    """Cria token JWT assinado com expiração configurável."""
    to_encode = user_data.copy()
    now = datetime.datetime.now(datetime.timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + datetime.timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    
    to_encode.update({
        "exp": expire,
        "iat": now,
        "sub": str(user_data.get("id"))
    })
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> Dict[str, Any]:
    """Decodifica e valida o token JWT."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise AuthError("Token inválido ou expirado")

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
) -> Dict[str, Any]:
    """
    Dependência injetada em rotas protegidas (/items/*, /me/*).
    Valida o header 'Authorization: Bearer <token>' e retorna { id, email, name }.
    """
    if not credentials or not credentials.credentials:
        raise AuthError("Token ausente ou malformado")
    
    payload = decode_access_token(credentials.credentials)
    user_id = payload.get("id") or payload.get("sub")
    email = payload.get("email")
    name = payload.get("name")
    
    if not user_id or not email:
        raise AuthError("Token inválido ou expirado")
        
    return {
        "id": int(user_id),
        "email": email,
        "name": name or ""
    }
