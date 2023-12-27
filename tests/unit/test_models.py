from app.main.models import Movie

# GIVEN a Movie model
# WHEN a new movie entry is created
# THEN check title, year, description, rating, review, img are defined correctly


def test_new_movie():
    movie = Movie(
        title="Titanic",
        year="1997",
        description="Greatest movie ever",
        rating=9.9,
        review="Recommend",
        img_url="xd.com",
    )

    assert movie.title == "Titanic"
    assert movie.year == "1997"
    assert movie.description == "Greatest movie ever"
    assert movie.rating == 9.9
    assert movie.review == "Recommend"
    assert movie.img_url == "xd.com"
