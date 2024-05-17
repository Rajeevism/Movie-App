from pydantic import BaseModel
from datetime import date


class Movie2 (BaseModel):
    id: int
    name: str
    language: str
    certificate: str
    imdb_rating: float
    image_url: str
    likes: int
    label: str
    genre: str
    movie_duration: int
    release_date: date
    about: str
