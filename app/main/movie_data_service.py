from app.main.models import Movie


# This class is responsible for updating (adding and deleting) movie database
class MovieDataService:
    def __init__(self, db):
        self.db = db

    def add_movie_to_db(self, movie_data):
        new_movie = Movie(
            title=movie_data["title"],
            year=movie_data["year"],
            description=movie_data["description"],
            img_url=movie_data["img_url"],
        )
        self.db.session.add(new_movie)
        self.db.session.commit()
        return new_movie

    def delete_movie(self, movie_id):
        movie_to_delete = self.db.get_or_404(Movie, movie_id)
        self.db.session.delete(movie_to_delete)
        self.db.session.commit()
