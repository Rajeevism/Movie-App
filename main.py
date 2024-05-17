from fastapi import FastAPI
from movie_app_controller import router as movie_router

app = FastAPI()

app.include_router(router=movie_router, prefix="/movies", tags=["movies"])
print(movie_router.routes)
