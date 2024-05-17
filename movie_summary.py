from pydantic import BaseModel


class MovieSummary (BaseModel):
    id: int
    name: str
    language: str
    certificate: str
    imdb_rating: float
    image_url: str
    likes: int
    label: str
