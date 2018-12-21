from tfidf.idf.idf_repository import CachedIdfRepository
from tfidf.tf.tf_movie import MovieTf


class MovieTfIdf:
    def __init__(self, movie_tf: MovieTf, idf_repository):
        self.movie_tf = movie_tf
        self.idf_repository = idf_repository

    def get_value(self, token: str) -> float:
        return self.movie_tf.get_tf(token) * self.idf_repository.find(token)
