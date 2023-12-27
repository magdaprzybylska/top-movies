import os
import datetime as dt
import requests


from app.main.models import Movie


MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
MOVIE_API_URL = "https://api.themoviedb.org/3"


class MovieService:
    def __init__(self, headers, db):
        self.headers = headers
        self.db = db

    def get_movie(self, movie_id):
        self.url = os.path.join(MOVIE_API_URL, "movie", f"{movie_id}?language=en-US")
        response = requests.get(self.url, headers=self.headers).json()
        release_date = response["release_date"]
        parsed_date = dt.datetime.strptime(release_date, "%Y-%m-%d")
        year = parsed_date.year
        new_movie = Movie(
            title=response["original_title"],
            year=year,
            description=response["overview"],
            img_url=f"{MOVIE_DB_IMAGE_URL}{response['poster_path']}",
        )
        self.db.session.add(new_movie)
        self.db.session.commit()
        return new_movie

    def get_movies_to_select(self, title):
        url = os.path.join(MOVIE_API_URL, "search", "movie")
        params = {"query": f"{title}"}
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            data = []
        else:
            response = response.json()
            data = response["results"]
        return data

    def delete_movie(self, movie_id):
        movie_to_delete = self.db.get_or_404(Movie, movie_id)
        self.db.session.delete(movie_to_delete)
        self.db.session.commit()
