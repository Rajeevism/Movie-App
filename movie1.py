from pydantic import BaseModel


class Movie1 (BaseModel):
    id: int
    name: str
    language: str
    certificate: str
    imdb_rating: float
    image_url: str
    likes: int
    label: str
