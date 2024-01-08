import datetime
import os
from unittest.mock import MagicMock, patch
import pytest

from app.main.api_caller import MovieApiCaller, MOVIE_DB_IMAGE_URL


@pytest.fixture
def api_caller():
    headers = {"Authorization": "Bearer your_token_here"}
    return MovieApiCaller(headers)


def test_get_movie(api_caller):
    # given
    response_data = {
        "original_title": "Movie Title",
        "release_date": "2022-01-01",
        "overview": "This is a movie overview",
        "poster_path": "/example_path.jpg",
    }
    mocked_response = MagicMock()
    mocked_response.json.return_value = response_data
    # when
    with patch("requests.get", return_value=mocked_response):
        movie_data = api_caller.get_movie(1)
    # then
    expected_result = {
        "title": response_data["original_title"],
        "year": 2022,
        "description": response_data["overview"],
        "img_url": f"{MOVIE_DB_IMAGE_URL}{response_data['poster_path']}",
    }

    assert movie_data == expected_result


def test_get_movies_to_select_success(api_caller):
    # given
    response_data = {"results": [{"title": "Movie 1"}, {"title": "Movie 2"}]}
    mocked_response = MagicMock()
    mocked_response.status_code = 200
    mocked_response.json.return_value = response_data

    # when
    with patch("requests.get", return_value=mocked_response):
        movies = api_caller.get_movies_to_select("query")
    # then
    expected_movies = [{"title": "Movie 1"}, {"title": "Movie 2"}]

    assert movies == expected_movies


def test_get_movies_to_select_failure(api_caller):
    mocked_response = MagicMock()
    mocked_response.status_code = 500

    with patch("requests.get", return_value=mocked_response):
        movies = api_caller.get_movies_to_select("query")

    expected_movies = []

    assert movies == expected_movies
