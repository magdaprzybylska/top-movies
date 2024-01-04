from app.main.models import Movie
from flask.testing import FlaskClient
from app import db
from tests.integration.page_objects_models.index import IndexPageObject


def test_verify_if_index_page_shows_movies(client: FlaskClient):
    # given
    new_movie = Movie(
        title="I love unicorn",
        year="1999",
        description="yolo",
        img_url="",
    )
    new_movie_2 = Movie(
        title="I love cats",
        year="2013",
        description="yolo",
        img_url="",
    )
    db.session.add(new_movie)
    db.session.add(new_movie_2)
    db.session.commit()
    # when
    response = client.get("/")
    # then
    page = IndexPageObject(response.data)
    actual_titles = page.get_top_10_titles()
    assert [new_movie.title, new_movie_2.title] == actual_titles


def test_verify_if_empty_db_doesnt_show_any_movie(client: FlaskClient):
    # when
    response = client.get("/")
    # then
    page = IndexPageObject(response.data)
    actual_titles = page.get_top_10_titles()
    assert [] == actual_titles
