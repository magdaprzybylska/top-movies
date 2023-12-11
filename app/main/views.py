from flask import render_template, request, redirect, url_for, current_app
from configparser import ConfigParser
import os

from app.main import bp
from app import db
from app.config import api
from app.main.models import Movie
from app.main.forms import MovieTitleForm, RatingForm
from app.main.movie_service import MovieService

# config = ConfigParser()
# config.read_dict(api)
# api_token = config['api']['api_token']
api_token = os.getenv("ACCESS_TOKEN_AUTH")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_token}",
}

movie_service = MovieService(headers, db)


@bp.route("/")
def home():
    movie_ratings = db.session.query(Movie.rating).all()
    movie_ratings.sort(reverse=True)

    movie_ratings = [(str(movie).strip("(),")) for movie in movie_ratings]

    # TODO add ranking functionality

    # for x in range(len(movie_rankings)):
    #     ranking = x + 1
    #     rating_str = str(movie_rankings[x]).strip("(),")
    #     rating = float(rating_str)
    #     movie_to_update = db.session.execute(
    #         db.select(Movie).where(Movie.rating == rating)
    #     ).scalar()
    #     movie_to_update.ranking = ranking
    #     db.session.commit()

    ranking = {}
    for count, movie_rating in enumerate(movie_ratings, 1):
        ranking[movie_rating] = count
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars()
    return render_template("index.html", movies=movies, rankings=ranking)


@bp.route("/edit", methods=["GET", "POST"])
def edit():
    form = RatingForm()
    movie_id = request.args.get("id")
    chosen_movie = db.get_or_404(Movie, movie_id)
    movie_title = chosen_movie.title
    if form.validate_on_submit():
        chosen_movie.rating = form.rating.data
        chosen_movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("edit.html", title=movie_title, form=form)


@bp.route("/delete", methods=["GET", "DELETE"])
def delete():
    movie_id = request.args.get("id")
    movie_service.delete_movie(movie_id)
    return redirect(url_for("main.home"))


@bp.route("/add", methods=["POST", "GET"])
def add():
    form = MovieTitleForm()
    if form.validate_on_submit():
        title = form.title.data
        api_data = movie_service.get_movies_to_select(title)
        return render_template("select.html", data=api_data)
    return render_template("add.html", form=form)


@bp.route("/find", methods=["GET", "POST"])
def find_movie():
    try:
        movie_id = int(request.args.get("id"))
        if movie_id is not None:
            new_movie = movie_service.get_movie(movie_id)
            return redirect(url_for("main.edit", id=new_movie.id))
        else:
            return render_template(
                "404.html",
                error="Unfortunatelly we could not find this movie in the TMDb database.",
            )
    except TypeError:
        return render_template(
            "404.html", error="Please provide valid movie ID. It must be an integer."
        )
