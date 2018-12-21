from typing import List, Set, Dict, Sequence
import math
from functional import seq
from tokenizer import simple_tokenizer


def get_idfs(movies_loader):
    print('get_idfs')
    return _get_idf_values(
        _count_movies_with_words(
            _load_words_by_movies(movies_loader)
        )
    )


def _get_idf_values(movies_containing_word: Dict[str, int]) -> Dict[str, float]:
    print('_get_idf_values')
    movies = len(movies_containing_word)
    return seq(movies_containing_word.items()) \
        .map(lambda item: (item[0], _get_idf_value(item[1], movies)))


def _get_idf_value(movies_containing_word, all_movies) -> float:
    return math.log10(all_movies / (1 + movies_containing_word))


def _count_movies_with_words(words_by_movies: Sequence[Set[str]]) -> Dict[str, int]:
    print('_count_movies_with_words')
    movies_containing_word = {}
    for index, movie in enumerate(words_by_movies):
        if index % 100 == 0: print(index)
        for word in movie:
            if word not in movies_containing_word:
                movies_containing_word[word] = 1
            else:
                movies_containing_word[word] += 1
    return movies_containing_word


def _load_words_by_movies(movies_loader) -> List[Set[str]]:
    print('_load_words_by_movies')
    return seq(movies_loader).map(_get_words_from_lines)


def _get_words_from_lines(lines: List[str]) -> Set[str]:
    words = set()
    for line in lines:
        words.update(_get_words_from_line(line))
    return words


def _get_words_from_line(line: str) -> Set[str]:
    return set(simple_tokenizer.tokenize(line))
