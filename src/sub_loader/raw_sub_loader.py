from typing import Tuple

MOVIE_SEPARATOR = '\n'
SUB_SEPARATOR = '|'


def load_full_by_movie(path, movies_to_load: int = None):
    with open(path) as file:
        subs = []
        movies = 0
        for line in file:
            if 'xml.gz' in line:
                continue
            if line == MOVIE_SEPARATOR:
                yield subs
                subs = []
                movies += 1
                if movies_to_load and movies == movies_to_load:
                    break
            else:
                subs.append(line.split(SUB_SEPARATOR)[0].strip())
        yield subs


def load_by_movie(path, movies_to_load: int = None):
    with open(path) as file:
        subs = []
        movies = 0
        for line in file:
            if 'xml.gz' in line:
                continue
            if line == MOVIE_SEPARATOR:
                yield subs
                subs = []
                movies += 1
                if movies_to_load and movies == movies_to_load:
                    break
            else:
                subs.append(line.split(SUB_SEPARATOR)[0].strip())
        yield subs


def load_with_times(path, movies_to_load: int = None):
    with open(path) as file:
        subs = []
        movies = 0
        for line in file:
            if 'xml.gz' in line:
                continue
            if line == MOVIE_SEPARATOR:
                yield subs
                subs = []
                movies += 1
                if movies_to_load and movies == movies_to_load:
                    break
            else:
                subs.append(create_subtitle(line))
        yield subs


class Subtitle:
    def __init__(self, text: str, time_start: int, time_end: int):
        self.text = text
        self.time_start = time_start
        self.time_end = time_end

    def __repr__(self):
        return ';'.join((self.text, str(self.time_start), str(self.time_end)))


def create_subtitle(line: str) -> Subtitle:
    splitted = line.split(SUB_SEPARATOR)

    time_start = None
    time_end = None
    if len(splitted) == 3:
        time_start = convert_to_millis(splitted[1])
        time_end = convert_to_millis(splitted[2].strip())
    if len(splitted) == 2:
        time_start = convert_to_millis(splitted[1].strip())

    return Subtitle(splitted[0].strip(), time_start, time_end)


def convert_to_millis(sub_time: str):
    try:
        full, millis = sub_time.split(',')
        hours, minutes, seconds = full.split(':')
        return int(millis) + 1000*(int(seconds) + 60 * int(minutes) + 3600 * int(hours))
    except Exception:
        return None
