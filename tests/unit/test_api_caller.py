import datetime
import os
from unittest.mock import Mock, patch
import pytest

from app.main.api_caller import MovieApiCaller


@pytest.fixture
def api_caller():
    headers = {"Authorization": "Bearer your_token_here"}
    return MovieApiCaller(headers)


def test_get_movie(api_caller):
    response_data = {
        "original_title": "Movie Title",
        "release_date": "2022-01-01",
        "overview": "This is a movie overview",
        "poster_path": "/example_path.jpg",
    }
    mocked_response = Mock()
    mocked_response.json.return_value = response_data

    with patch("requests.get", return_value=mocked_response):
        movie_data = api_caller.get_movie(1)

    expected_result = {
        "title": response_data["original_title"],
        "year": 2022,
        "description": response_data["overview"],
        "img_url": "https://image.tmdb.org/t/p/w500/example_path.jpg",
    }

    assert movie_data == expected_result


def test_get_movies_to_select_success(api_caller):
    response_data = {"results": [{"title": "Movie 1"}, {"title": "Movie 2"}]}
    mocked_response = Mock()
    mocked_response.status_code = 200
    mocked_response.json.return_value = response_data

    with patch("requests.get", return_value=mocked_response):
        movies = api_caller.get_movies_to_select("query")

    expected_movies = [{"title": "Movie 1"}, {"title": "Movie 2"}]

    assert movies == expected_movies


def test_get_movies_to_select_failure(api_caller):
    mocked_response = Mock()
    mocked_response.status_code = 500

    with patch("requests.get", return_value=mocked_response):
        movies = api_caller.get_movies_to_select("query")

    expected_movies = []

    assert movies == expected_movies
