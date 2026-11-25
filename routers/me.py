from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from schemas import ItemSummary, FavoriteActionResponse, ErrorResponse
from database import supabase
from security import get_current_user

router = APIRouter(prefix="/me", tags=["Minha Conta & Favoritos"])

@router.get(
    "/favorites",
    response_model=List[ItemSummary],
    responses={401: {"model": ErrorResponse, "description": "Não autorizado"}},
    summary="Listar Obras Favoritas do Usuário Autenticado"
)
async def list_my_favorites(
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna todas as obras favoritadas pelo aluno autenticado,
    ordenadas das mais recentemente adicionadas para as mais antigas.
    """
    user_id = current_user["id"]
    try:
        fav_resp = (
            supabase.table("favorites")
            .select("item_id, created_at, items(*)")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        data = fav_resp.data or []
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao consultar favoritos: {str(e)}"
        )

    if not data:
        return []

    item_ids = [row["item_id"] for row in data if row.get("items")]

    # Busca avaliações para calcular média
    ratings_by_item = {i_id: [] for i_id in item_ids}
    if item_ids:
        try:
            rev_resp = (
                supabase.table("reviews")
                .select("item_id, rating")
                .in_("item_id", item_ids)
                .execute()
            )
            for r in (rev_resp.data or []):
                ratings_by_item[r["item_id"]].append(r["rating"])
        except Exception:
            pass

    favorites_list = []
    for row in data:
        item = row.get("items")
        if not item:
            continue
        ratings = ratings_by_item.get(item["id"], [])
        avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0.0
        favorites_list.append({
            "id": item["id"],
            "title": item["title"],
            "synopsis": item["synopsis"],
            "category": item["category"],
            "release_year": item["release_year"],
            "poster_url": item["poster_url"],
            "created_at": item.get("created_at"),
            "is_favorite": True,
            "average_rating": avg_rating
        })

    return favorites_list

@router.post(
    "/favorites/{item_id}",
    response_model=FavoriteActionResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Não autorizado"},
        404: {"model": ErrorResponse, "description": "Obra não encontrada"}
    },
    summary="Adicionar Obra aos Favoritos (Idempotente)"
)
async def add_favorite(
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Adiciona a obra aos favoritos do usuário autenticado.
    Garante idempotência (cliques duplos rápidos não causam erro 500).
    """
    # Checa se o item existe
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
    try:
        # Upsert com ignore_duplicates para ON CONFLICT DO NOTHING
        supabase.table("favorites").upsert(
            {"user_id": user_id, "item_id": item_id},
            on_conflict="user_id,item_id",
            ignore_duplicates=True
        ).execute()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao favoritar obra: {str(e)}"
        )

    return {
        "message": "Obra adicionada aos favoritos com sucesso",
        "item_id": item_id,
        "is_favorite": True
    }

@router.delete(
    "/favorites/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Não autorizado"}
    },
    summary="Remover Obra dos Favoritos"
)
async def remove_favorite(
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Remove a obra da lista de favoritos do usuário autenticado.
    Retorna 204 No Content.
    """
    user_id = current_user["id"]
    try:
        supabase.table("favorites").delete().eq("user_id", user_id).eq("item_id", item_id).execute()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao desfavoritar obra: {str(e)}"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
