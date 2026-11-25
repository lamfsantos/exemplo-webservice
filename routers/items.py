import math
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas import (
    ItemListResponse,
    ItemDetail,
    ItemSummary,
    ReviewCreate,
    ReviewResponse,
    ErrorResponse
)
from database import supabase
from security import get_current_user

router = APIRouter(prefix="/items", tags=["Obras (Catálogo)"])

@router.get(
    "",
    response_model=ItemListResponse,
    responses={401: {"model": ErrorResponse, "description": "Não autorizado"}},
    summary="Listar Obras com Paginação, Busca e Filtro"
)
async def list_items(
    page: int = Query(1, ge=1, description="Número da página (inicia em 1)"),
    limit: int = Query(10, ge=1, le=50, description="Itens por página (máx: 50)"),
    search: Optional[str] = Query(None, description="Busca textual por título"),
    category: Optional[str] = Query(None, description="Filtro por categoria exata"),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna catálogo paginado de obras.
    Inclui status de favorito (`is_favorite`) para o usuário autenticado e a média de avaliações (`average_rating`).
    """
    offset = (page - 1) * limit
    to_idx = offset + limit - 1

    query = supabase.table("items").select("*", count="exact")

    if category:
        query = query.eq("category", category.strip())

    if search:
        query = query.ilike("title", f"%{search.strip()}%")

    query = query.order("id").range(offset, to_idx)

    try:
        response = query.execute()
        items_data = response.data or []
        total = response.count if response.count is not None else len(items_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar obras: {str(e)}"
        )

    last_page = math.ceil(total / limit) if total > 0 else 1

    if not items_data:
        return {
            "items": [],
            "total": total,
            "page": page,
            "limit": limit,
            "last_page": last_page
        }

    item_ids = [item["id"] for item in items_data]
    user_id = current_user["id"]

    # 1. Busca favoritos do usuário atual para estes itens (Batch)
    user_favorites = set()
    try:
        fav_resp = (
            supabase.table("favorites")
            .select("item_id")
            .eq("user_id", user_id)
            .in_("item_id", item_ids)
            .execute()
        )
        if fav_resp.data:
            user_favorites = {f["item_id"] for f in fav_resp.data}
    except Exception:
        pass

    # 2. Busca reviews para calcular médias (Batch)
    ratings_by_item = {item_id: [] for item_id in item_ids}
    try:
        rev_resp = (
            supabase.table("reviews")
            .select("item_id, rating")
            .in_("item_id", item_ids)
            .execute()
        )
        if rev_resp.data:
            for r in rev_resp.data:
                ratings_by_item[r["item_id"]].append(r["rating"])
    except Exception:
        pass

    # 3. Monta o payload final
    summaries = []
    for item in items_data:
        ratings = ratings_by_item.get(item["id"], [])
        avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0.0
        summaries.append({
            "id": item["id"],
            "title": item["title"],
            "synopsis": item["synopsis"],
            "category": item["category"],
            "release_year": item["release_year"],
            "poster_url": item["poster_url"],
            "created_at": item.get("created_at"),
            "is_favorite": item["id"] in user_favorites,
            "average_rating": avg_rating
        })

    return {
        "items": summaries,
        "total": total,
        "page": page,
        "limit": limit,
        "last_page": last_page
    }

@router.get(
    "/{item_id}",
    response_model=ItemDetail,
    responses={
        401: {"model": ErrorResponse, "description": "Não autorizado"},
        404: {"model": ErrorResponse, "description": "Obra não encontrada"}
    },
    summary="Detalhes de uma Obra com Avaliações"
)
async def get_item_detail(
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna os dados completos da obra, se é favorita do usuário atual,
    sua nota média e todas as avaliações com o nome do avaliador ordenadas por data desc.
    """
    try:
        resp = supabase.table("items").select("*").eq("id", item_id).execute()
        if not resp.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Obra não encontrada"
            )
        item = resp.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar detalhes da obra: {str(e)}"
        )

    user_id = current_user["id"]

    # Verifica se é favorito do usuário atual
    is_favorite = False
    try:
        fav_resp = (
            supabase.table("favorites")
            .select("item_id")
            .eq("user_id", user_id)
            .eq("item_id", item_id)
            .execute()
        )
        is_favorite = len(fav_resp.data or []) > 0
    except Exception:
        pass

    # Busca avaliações com dados do usuário
    reviews_formatted = []
    ratings = []
    try:
        rev_resp = (
            supabase.table("reviews")
            .select("id, user_id, rating, comment, created_at, users(name)")
            .eq("item_id", item_id)
            .order("created_at", desc=True)
            .execute()
        )
        for r in (rev_resp.data or []):
            ratings.append(r["rating"])
            user_info = r.get("users") or {}
            user_name = user_info.get("name") if isinstance(user_info, dict) else None
            reviews_formatted.append({
                "id": r["id"],
                "user_id": r["user_id"],
                "user_name": user_name or f"Aluno #{r['user_id']}",
                "rating": r["rating"],
                "comment": r.get("comment"),
                "created_at": r.get("created_at")
            })
    except Exception:
        # Fallback sem join se RLS ou foreign table falhar
        try:
            rev_fallback = (
                supabase.table("reviews")
                .select("id, user_id, rating, comment, created_at")
                .eq("item_id", item_id)
                .order("created_at", desc=True)
                .execute()
            )
            for r in (rev_fallback.data or []):
                ratings.append(r["rating"])
                reviews_formatted.append({
                    "id": r["id"],
                    "user_id": r["user_id"],
                    "user_name": f"Aluno #{r['user_id']}",
                    "rating": r["rating"],
                    "comment": r.get("comment"),
                    "created_at": r.get("created_at")
                })
        except Exception:
            pass

    avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0.0

    return {
        "id": item["id"],
        "title": item["title"],
        "synopsis": item["synopsis"],
        "category": item["category"],
        "release_year": item["release_year"],
        "poster_url": item["poster_url"],
        "created_at": item.get("created_at"),
        "is_favorite": is_favorite,
        "average_rating": avg_rating,
        "reviews": reviews_formatted
    }

@router.post(
    "/{item_id}/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse, "description": "Não autorizado"},
        404: {"model": ErrorResponse, "description": "Obra não encontrada"}
    },
    summary="Avaliar Obra (Criar ou Atualizar Nota)"
)
async def create_or_update_review(
    item_id: int,
    review_in: ReviewCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Cria ou atualiza (UPSERT) a avaliação de uma obra pelo aluno autenticado.
    Se o aluno já tiver avaliado a obra, atualiza nota e comentário sem estourar erro de duplicidade.
    """
    # Verifica se a obra existe
    try:
        check = supabase.table("items").select("id").eq("id", item_id).execute()
        if not check.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Obra não encontrada"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao verificar obra: {str(e)}"
        )

    user_id = current_user["id"]
    review_payload = {
        "user_id": user_id,
        "item_id": item_id,
        "rating": review_in.rating,
        "comment": review_in.comment.strip() if review_in.comment else None
    }

    try:
        res = (
            supabase.table("reviews")
            .upsert(review_payload, on_conflict="user_id,item_id")
            .execute()
        )
        saved = res.data[0] if res.data else review_payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar avaliação: {str(e)}"
        )

    return {
        "id": saved.get("id", 0),
        "user_id": user_id,
        "user_name": current_user.get("name") or f"Aluno #{user_id}",
        "rating": saved.get("rating", review_in.rating),
        "comment": saved.get("comment"),
        "created_at": saved.get("created_at")
    }
