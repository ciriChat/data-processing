from functional import seq
from morph import morph_repository
from typing import List

polimorf_file_path = '../resources/PoliMorf-0.6.7.tab'
polimorf_file_path_v2 = '../resources/polimorfologik-2.1.txt'


def load_polimorf(path):
    with open(path) as file:
        return file.readlines()


class PolimorfLine:
    def __init__(self, word, base_form, tags, category=None):
        self.word = word
        self.base_form = base_form
        self.tags = tags
        self.category = category


class PolimorfFactory:
    @staticmethod
    def from_line(line: str) -> PolimorfLine or None:
        line = line.strip()
        splitted = line.split('\t')
        if len(splitted) == 3:
            return PolimorfLine(splitted[0], splitted[1], splitted[2])
        elif len(splitted) == 4:
            return PolimorfLine(splitted[0], splitted[1], splitted[2], splitted[3])
        return None

    @staticmethod
    def from_line_v2(line: str) -> List[PolimorfLine] or None:
        line = line.strip()
        splitted = line.split(';')
        lines = []
        for tag in splitted[2].split('+'):
            lines.append(PolimorfLine(splitted[1], splitted[0], tag))
        return lines


def insert_v1():
    res = seq(load_polimorf(polimorf_file_path)) \
        .map(PolimorfFactory.from_line) \
        .filter(lambda l: l) \
        .map(lambda line: (line.word, line.base_form, line.tags, line.category))

    morph_repository.insert(res)


def insert_v2():
    res = seq(load_polimorf(polimorf_file_path_v2)) \
        .flat_map(PolimorfFactory.from_line_v2) \
        .filter(lambda l: l) \
        .map(lambda line: (line.word, line.base_form, line.tags))

    morph_repository.insert_v2(res)


if __name__ == '__main__':
    insert_v2()