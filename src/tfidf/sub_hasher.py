from sub.sub_repository import sub_repository
from sub_loader import raw_sub_loader
from config import file_config
from tfidf.idf.idf_repository import CachedIdfRepository
from tfidf.tf.tf_movie import MovieTf
from tfidf.movie_tf_df import MovieTfIdf

from tokenizer import simple_tokenizer
from functional import seq
from typing import List


def hash_subtitles():
    movies = raw_sub_loader.load_with_times(file_config['subtitles_with_times_path'])
    movie_id = 0
    idf_repository = CachedIdfRepository()

    to_save = []

    for movie in movies:
        print(movie_id)
        movie_id += 1
        if movie_id < 30000:
            continue

        movieTf = MovieTf(movie)
        movieTfIdf = MovieTfIdf(movieTf, idf_repository)
        sub_tokens_factory = SubTokensFactory(movieTfIdf)

        for sub in movie:
            if len(sub.text) > 1000:
                continue

            try:
                sub_tokens = sub_tokens_factory.from_sub(sub.text)
                hash1 = sub_tokens.get_hash(1)
                hash2 = sub_tokens.get_hash(2)
                hash3 = sub_tokens.get_hash(3)
                if len(hash1) > 50 or len(hash2) > 100 or len(hash3) > 150:
                    continue
                to_save.append((sub.text, sub.time_start, sub.time_end, hash1, hash2, hash3))
            except Exception:
                print('error')

        if movie_id % 100 == 0:
            try:
                sub_repository.save_sub(to_save)
                to_save = []
            except Exception:
                print("except")

    if to_save:
        try:
            sub_repository.save_sub(to_save)
        except Exception:
            print("except")


class SubTokensFactory:
    def __init__(self, movie_tf_idf: MovieTfIdf):
        self.movie_tf_idf = movie_tf_idf

    def from_sub(self, sub: str):
        tokens = simple_tokenizer.tokenize(sub)
        sub_tokens = []
        for index, token in enumerate(tokens):
            sub_tokens.append(SubToken(token, index, self.movie_tf_idf.get_value(token)))

        return SubTokens(sub_tokens)


class SubToken:
    def __init__(self, token, index, tf_idf):
        self.token = token
        self.index = index
        self.tf_idf = tf_idf


class SubTokens:
    def __init__(self, tokens: List[SubToken]):
        self.tokens: List[SubToken] = seq(tokens).order_by(lambda token: -token.tf_idf).to_list()

    def get_hash(self, n: int) -> str:
        tokens = seq(self.tokens).take(n)\
            .order_by(lambda token: token.index)\
            .map(lambda token: token.token)\
            .to_list()

        return HashFactory.get_hash(tokens)


class HashFactory:
    HASH_SEPARATOR = '_'

    @classmethod
    def get_hash(cls, tokens: List[str]):
        return cls.HASH_SEPARATOR.join(tokens)


if __name__ == '__main__':
    hash_subtitles()
