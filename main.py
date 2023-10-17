from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

db = SQLAlchemy()
load_dotenv()

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN_AUTH')}"
}
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    year = db.Column(db.Integer)
    description = db.Column(db.String)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String)
    img_url = db.Column(db.String)


class MyForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db.init_app(app)
Bootstrap5(app)


@app.route("/", methods=['GET', 'POST'])
def home():
    with app.app_context():
        movie_rankings = db.session.query(Movie.rating).all()
        movie_rankings.sort(reverse=True)

        for x in range(len(movie_rankings)):
            ranking = x + 1
            rating_str = str(movie_rankings[x]).strip('(),')
            rating = float(rating_str)
            movie_to_update = db.session.execute(db.select(Movie).where(Movie.rating == rating)).scalar()
            movie_to_update.ranking = ranking
            db.session.commit()

        movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars()

        return render_template("index.html", movies=movies)


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    movie_id = request.args.get('id')
    if request.method == 'POST':
        with app.app_context():
            movie_to_update = db.get_or_404(Movie, movie_id)
            movie_to_update.rating = request.form['rating']
            movie_to_update.review = request.form['review']
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('edit.html')


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    movie_id = request.args.get('id')
    with app.app_context():
        movie_to_delete = db.get_or_404(Movie, movie_id)
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect(url_for('home'))


@app.route("/add", methods=['POST', 'GET'])
def add():
    form = MyForm()
    if form.validate_on_submit():
        title = form.title.data
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            'query': f'{title}'
        }
        response = requests.get(url, headers=headers, params=params).json()
        data = response['results']
        return render_template('select.html', data=data)

    return render_template('add.html', form=form)


@app.route('/find', methods=['GET', 'POST'])
def find_movie():
    movie_id = int(request.args.get('id'))
    if movie_id is not None:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        response = requests.get(url, headers=headers).json()

        with app.app_context():
            new_movie = Movie(
                title=response['original_title'],
                year=response['release_date'][:4],
                description=response['overview'],
                img_url=f"{MOVIE_DB_IMAGE_URL}{response['poster_path']}"
            )
            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for('edit', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)