from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired


class MovieTitleForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])


class RatingForm(FlaskForm):
    rating = FloatField("Your rating", validators=[DataRequired()])
    review = StringField("Your review", validators=[DataRequired()])
