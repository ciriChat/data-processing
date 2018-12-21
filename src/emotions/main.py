from emotions.insert import insert
nawl_path = '../resources/nawl-analysis.csv'


def load_nawl(path):
    with open(path) as file:
        return file.readlines()

def clean_word(word: str):
    return word.replace('"', '')


if __name__ == '__main__':
    lines = load_nawl(nawl_path)
    lines.pop(0)

    to_insert = []
    for line in lines:
        splitted = line.split(',')
        to_insert.append((clean_word(splitted[0]), splitted[1], float(splitted[2]), float(splitted[3]), float(splitted[4]), float(splitted[5]), float(splitted[6])))

    insert(to_insert)