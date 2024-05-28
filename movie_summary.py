from pydantic import BaseModel


class MovieSummary (BaseModel):
    id: int
    image_url: str
    movie_name: str
    certificate: str
    likes: int
    languages: list  # type: ignore
