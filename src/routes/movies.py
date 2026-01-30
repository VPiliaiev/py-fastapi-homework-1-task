import math
from fastapi import Request
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from database import MovieModel

from schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.get("/", response_model=MovieListResponseSchema)
async def read_movies(
        request: Request,
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20)
):
    count_stmt = select(func.count()).select_from(MovieModel)
    total_items = (await db.execute(count_stmt)).scalar_one()
    if total_items == 0:
        raise HTTPException(404, "No movies found.")
    total_pages = math.ceil(total_items / per_page)
    if page > total_pages:
        raise HTTPException(404, "No movies found.")
    offset = (page - 1) * per_page
    stmt = select(MovieModel).limit(per_page).offset(offset)
    result = await db.execute(stmt)
    items = result.scalars().all()
    base_url = request.url.path
    prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"{base_url}?page={page + 1}&per_page={per_page}" if page < total_pages else None
    movies = [
        MovieDetailResponseSchema.model_validate(movie, from_attributes=True)
        for movie in items
    ]
    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def read_movie(
        movie_id: int,
        db: AsyncSession = Depends(get_db),
):
    stmt = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(stmt)
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
