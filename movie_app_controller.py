from fastapi import APIRouter, HTTPException
import pymysql
import pymysql.cursors
from artist import Artist
from movie_summary import MovieSummary
from movie_details import MovieDetails


router = APIRouter()

connection = pymysql.connect(
    host="localhost",
    user="rajeev",
    password="Rajeev2005",
    database="movie_app_db",
    cursorclass=pymysql.cursors.DictCursor,
)


@router.get(path="", response_model=list[MovieSummary])
def get_all_movies():
    with connection.cursor() as cursor:
        query = '''SELECT m.id,image_url, m.name, certificate, imdb_rating, m.likes, l.language, f.label
        FROM movie_app_db.movies as m
        INNER JOIN movie_app_db.language as l
        ON m.language_id = l.id
        INNER JOIN movie_app_db.format as f
        ON m.format_id = f.id'''
        cursor.execute(query=query)
        movies = cursor.fetchall()
        return movies


@router.get(path="/{movie_id}", response_model=MovieDetails | dict[str, str])
def get_movie_by_id(movie_id: str) -> MovieDetails | dict[str, str]:
    with connection.cursor() as cursor:
        query = '''SELECT m.id, m.image_url, m.movie_name,l.language,m.certificate,m.imdb_rating,m.likes,f.label,
	    g.genre,m.movie_duration,m.release_date,m.about 
        FROM movie_app_db.movies m 
        INNER JOIN movie_app_db.language as l ON m.language_id = l.id
	    INNER JOIN movie_app_db.format as f ON m.format_id = f.id
	    INNER JOIN movie_app_db.movie_genre as mg ON mg.movie_id=m.id
	    INNER JOIN movie_app_db.genre as g  ON mg.genre_id=g.id
        WHERE m.id=%s'''
        cursor.execute(query=query, args=movie_id)
        movie = cursor.fetchone()
        if movie == None:
            raise HTTPException(status_code=404, detail="Movie not found")
        query = '''SELECT ar.image_url,ar.name,r.role
	    FROM movie_app_db.movie_artists ma 
        inner join role r on ma.role_id = r.id
        inner join artists ar on ma.artists_id = ar.id
        WHERE ma.movie_id=%s'''
        cursor.execute(query=query, args=movie_id)
        artists = cursor.fetchall()
        artistList = list[Artist]()
        for artist in artists:
            artistList.append(artist)  # type: ignore
        movie["artists"] = artistList
        return movie
