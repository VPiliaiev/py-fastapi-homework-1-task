from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MovieBase(BaseModel):
    id: int
    name: str
    date: date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str


class MovieDetailResponseSchema(MovieBase):
    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
    model_config = ConfigDict(from_attributes=True)
