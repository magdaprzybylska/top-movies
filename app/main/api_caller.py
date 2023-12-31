import os
import datetime as dt
import requests

MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
MOVIE_API_URL = "https://api.themoviedb.org/3"


# This class is responsible for making API requests and returning fetched data in dict format
class MovieApiCaller:
    def __init__(self, headers):
        self.headers = headers

    def make_request(self, url, params=None):
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()

    def get_movie(self, movie_id):
        url = os.path.join(MOVIE_API_URL, "movie", f"{movie_id}?language=en-US")
        response = self.make_request(url)
        release_date = response["release_date"]
        parsed_date = dt.datetime.strptime(release_date, "%Y-%m-%d")
        year = parsed_date.year

        new_movie_data = {
            "title": response["original_title"],
            "year": year,
            "description": response["overview"],
            "img_url": f"{MOVIE_DB_IMAGE_URL}{response['poster_path']}",
        }

        return new_movie_data

    def get_movies_to_select(self, title):
        url = os.path.join(MOVIE_API_URL, "search", "movie")
        params = {"query": f"{title}"}
        response = self.make_request(url, params=params)
        if response.status_code != 200:
            data = []
        else:
            response = response.json()
            data = response["results"]
        return data
