from pydantic import BaseModel


class Artist(BaseModel):
    image_url: str
    name: str
    role: str
