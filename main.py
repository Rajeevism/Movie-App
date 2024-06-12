from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from movie_app_controller import router as movie_router

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=movie_router, prefix="/movies", tags=["movies"])
print(movie_router.routes)
