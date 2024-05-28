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
def get_all_movies():  # type: ignore
    with connection.cursor() as cursor:
        query = "SELECT id,image_url, movie_name, certificate, likes FROM movie_app_db.movies"
        cursor.execute(query=query)
        movies = cursor.fetchall()
        query = '''SELECT m.id as movie_id, l.language FROM movie_app_db.movies m
                INNER JOIN movie_app_db.movie_language ml ON ml.movie_id = m.id
                INNER JOIN movie_app_db.language l ON ml.language_id = l.id'''
        cursor.execute(query=query)
        languages = cursor.fetchall()
        result = []
        for movie in movies:
            languageList = filter(  # type: ignore
                lambda x: x['movie_id'] == movie['id'], languages)  # type: ignore
            langList = list(languageList)  # type: ignore
            print(langList)  # type: ignore
            langs = []
            for lang in langList:  # type: ignore
                langs.append(lang['language'])  # type: ignore
            movie["languages"] = langs  # type: ignore
            result.append(movie)  # type: ignore
        return result  # type: ignore


@router.get(path="/{movie_id}", response_model=MovieDetails | dict[str, str])
def get_movie_by_id(movie_id: str) -> MovieDetails | dict[str, str]:
    with connection.cursor() as cursor:
        query = '''SELECT DISTINCT m.id, m.image_url, m.movie_name,m.certificate,m.imdb_rating,m.likes,
	    g.genre,m.movie_duration,m.release_date,m.about,u.user_name,re.reviews,re.rating,re.likes,re.review_date
		FROM movie_app_db.user_movie_review umr
        INNER JOIN movie_app_db.movies m ON umr.movie_id = m.id
		INNER JOIN movie_app_db.users u ON umr.user_id = u.id	
        INNER JOIN movie_app_db.reviews re ON umr.review_id = re.id
	    INNER JOIN movie_app_db.movie_genre as mg ON mg.movie_id=m.id
	    INNER JOIN movie_app_db.genre as g  ON mg.genre_id=g.id
        WHERE m.id =%s'''
        cursor.execute(query=query, args=movie_id)
        movie = cursor.fetchone()
        if movie == None:
            raise HTTPException(status_code=404, detail="Movie not found")
        query = '''SELECT l.language FROM movie_app_db.movie_language ml
	            INNER JOIN movie_app_db.movies m ON ml.movie_id = m.id
                INNER JOIN movie_app_db.language l ON ml.language_id = l.id
                WHERE ml.movie_id =%s'''
        cursor.execute(query=query, args=movie_id)
        languages = cursor.fetchall()
        print(languages)

        langList = []
        for lang in languages:
            langList.append(lang)  # type: ignore
        movie["languages"] = langList
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
