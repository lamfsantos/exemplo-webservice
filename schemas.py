from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# =====================================================================
# Auth Schemas
# =====================================================================
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="teste@app.com")
    password: str = Field(..., min_length=1, example="123456")

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=120, example="Maria Silva")
    email: EmailStr = Field(..., example="maria@estudante.ifms.edu.br")
    password: str = Field(..., min_length=6, example="123456")

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class AuthResponse(BaseModel):
    token: str
    user: UserResponse

# Alias para compatibilidade
LoginResponse = AuthResponse

# =====================================================================
# Review Schemas
# =====================================================================
class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Nota de 1 a 5 estrelas", example=5)
    comment: Optional[str] = Field(None, description="Comentário sobre a obra", example="Excelente filme, recomendo muito!")

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    user_name: Optional[str] = None
    rating: int
    comment: Optional[str] = None
    created_at: Optional[str] = None

# =====================================================================
# Item Schemas
# =====================================================================
class ItemBase(BaseModel):
    id: int
    title: str
    synopsis: str
    category: str
    release_year: int
    poster_url: str
    created_at: Optional[str] = None

class ItemSummary(ItemBase):
    is_favorite: bool = False
    average_rating: float = 0.0

class ItemDetail(ItemSummary):
    reviews: List[ReviewResponse] = []

class PaginationMeta(BaseModel):
    current_page: int = Field(..., example=1)
    last_page: int = Field(..., example=5)
    total: int = Field(..., example=43)
    limit: int = Field(10, example=10)

class ItemListResponse(BaseModel):
    # Formato do enunciado do desafio mobile:
    data: List[ItemSummary]
    meta: PaginationMeta
    # Aliases de compatibilidade para quem consumir chaves de primeiro nível:
    items: List[ItemSummary]
    total: int
    page: int
    limit: int
    last_page: int

# =====================================================================
# Favorite Schemas
# =====================================================================
class FavoriteActionResponse(BaseModel):
    message: str
    item_id: int
    is_favorite: bool

# =====================================================================
# Generic / Health
# =====================================================================
class HealthResponse(BaseModel):
    status: str = "ok"

class ErrorResponse(BaseModel):
    error: str
