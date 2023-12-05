from flask import render_template, request, redirect, url_for
import requests
import os
from datetime import datetime

from app.main import bp
from app import db
from app.main.models import Movie
from app.main.forms import MovieTitleForm


headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN_AUTH')}",
}

MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
MOVIE_API_URL = "https://api.themoviedb.org/3"


@bp.route("/")
def home():
    movie_rankings = db.session.query(Movie.rating).all()
    movie_rankings.sort(reverse=True)

    for x in range(len(movie_rankings)):
        ranking = x + 1
        rating_str = str(movie_rankings[x]).strip("(),")
        rating = float(rating_str)
        movie_to_update = db.session.execute(
            db.select(Movie).where(Movie.rating == rating)
        ).scalar()
        movie_to_update.ranking = ranking
        db.session.commit()

    movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars()

    return render_template("index.html", movies=movies)


@bp.route("/edit", methods=["GET", "POST"])
def edit():
    movie_id = request.args.get("id")
    chosen_movie = db.get_or_404(Movie, movie_id)
    movie_title = chosen_movie.title
    if request.method == "POST":
        chosen_movie.rating = request.form["rating"]
        chosen_movie.review = request.form["review"]
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("edit.html", title=movie_title)


@bp.route("/delete", methods=["GET", "POST"])
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("main.home"))


@bp.route("/add", methods=["POST", "GET"])
def add():
    form = MovieTitleForm()
    if form.validate_on_submit():
        title = form.title.data
        url = os.path.join(MOVIE_API_URL, "search", "movie")
        params = {"query": f"{title}"}
        response = requests.get(url, headers=headers, params=params).json()
        data = response["results"]
        return render_template("select.html", data=data)

    return render_template("add.html", form=form)


@bp.route("/find", methods=["GET", "POST"])
def find_movie():
    movie_id = int(request.args.get("id"))
    if movie_id is not None:
        url = os.path.join(MOVIE_API_URL, "movie", f"{movie_id}?language=en-US")
        response = requests.get(url, headers=headers).json()
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
        return redirect(url_for("main.edit", id=new_movie.id))
