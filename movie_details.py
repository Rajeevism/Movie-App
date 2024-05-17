from pydantic import BaseModel
from datetime import date

from artist import Artist


class MovieDetails (BaseModel):
    id: int
    movie_name: str
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
    artists: list[Artist]
