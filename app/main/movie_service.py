import os
import datetime
import requests

from app import db
from app.main.models import Movie

# is it ok to import database inside this module?

MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
MOVIE_API_URL = "https://api.themoviedb.org/3"


class MovieService:
    def __init__(self, headers):
        self.headers = headers

    def get_movie(self, movie_id):
        self.url = os.path.join(MOVIE_API_URL, "movie", f"{movie_id}?language=en-US")
        response = requests.get(self.url, headers=self.headers).json()
        release_date = response["release_date"]
        parsed_date = datetime.strptime(release_date, "%Y-%m-%d")
        year = parsed_date.year
        new_movie = Movie(
            title=response["original_title"],
            year=year,
            description=response["overview"],
            img_url=f"{MOVIE_DB_IMAGE_URL}{response['poster_path']}",
        )
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    def get_movies_to_select(self, title):
        self.url = os.path.join(MOVIE_API_URL, "search", "movie")
        params = {"query": f"{title}"}
        response = requests.get(self.url, headers=self.headers, params=params).json()
        data = response["results"]
        return data


# add try and except to this funtion, try movie_id(int)
