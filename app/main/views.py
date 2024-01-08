from flask import render_template, request, redirect, url_for
import os

from app.main import bp
from app import db

from app.main.models import Movie
from app.main.forms import MovieTitleForm, RatingForm
from app.main.movie_data_service import MovieDataService
from app.main.api_caller import MovieApiCaller


api_token = os.getenv("ACCESS_TOKEN_AUTH")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_token}",
}

data_service = MovieDataService(db)
api_caller = MovieApiCaller(headers)


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


@bp.route("/edit/<movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    form = RatingForm()
    chosen_movie = db.get_or_404(Movie, movie_id)
    movie_title = chosen_movie.title
    if form.validate_on_submit():
        chosen_movie.rating = form.rating.data
        chosen_movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("edit.html", title=movie_title, form=form)


@bp.route("/add", methods=["POST", "GET"])
def add():
    form = MovieTitleForm()
    if form.validate_on_submit():
        title = form.title.data
        api_data = api_caller.get_movies_to_select(title)
        print()
        return render_template("select.html", data=api_data)
    return render_template("add.html", form=form)


@bp.route("/find", methods=["GET", "POST"])
def find_movie():
    try:
        movie_id = request.args.get("id")
        if movie_id is not None:
            api_data = api_caller.get_movie(movie_id)
            new_movie = data_service.add_movie_to_db(api_data)
            return redirect(url_for("main.edit", movie_id=new_movie.id))
        else:
            return render_template(
                "404.html",
                error="Unfortunatelly we could not find this movie in the TMDb database.",
            )
    except TypeError:
        return render_template(
            "404.html", error="Please provide valid movie ID. It must be an integer."
        )


@bp.route("/delete/<movie_id>", methods=["GET", "POST"])
def delete(movie_id):
    if request.form.get("_method") == "DELETE":
        data_service.delete_movie(movie_id)
        return redirect(url_for("main.home"))
    else:
        return render_template("404.html", error="Invalid method.")
