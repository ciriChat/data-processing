from config import file_config
from sub_loader import raw_sub_loader

from tfidf.idf import idf, idf_repository

if __name__ == '__main__':
    movies = raw_sub_loader.load_by_movie(file_config['subtitles_with_times_path'])
    movies_idf = idf.get_idfs(movies)
    print('start inserting')
    idf_repository.insert(movies_idf)
