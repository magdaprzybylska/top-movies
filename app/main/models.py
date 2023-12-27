from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so


class Movie(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True)
    year: so.Mapped[int] = so.mapped_column(sa.Integer())
    description: so.Mapped[str] = so.mapped_column(sa.String(500))
    rating: so.Mapped[float] = so.mapped_column(sa.Float(3), nullable=True)
    review: so.Mapped[str] = so.mapped_column(sa.String(500), nullable=True)
    img_url: so.Mapped[str] = so.mapped_column(sa.String(500))

    def __repr__(self):
        return "<Movie {}".format(self.title)
