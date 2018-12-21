from db.mysql_db import get_connection
from typing import List, Tuple, Sequence


_connection = get_connection('pl_subtitles_db')

BATCH_SIZE = 10000

INSERT_QUERY = '''
    INSERT INTO morph_dict_pl(word, base_form, tags, category) VALUES(%s, %s, %s, %s)
'''

INSERT_QUERY_V2 = '''
    INSERT INTO morph_dict_pl_2(word, base_form, tags) VALUES(%s, %s, %s)
'''


def insert(morphs: Sequence[Tuple[str, str, str, str]]):
    cursor = _connection.cursor()

    batch = []
    for morph in morphs:
        batch.append(morph)
        if len(batch) % BATCH_SIZE == 0:
            try:
                cursor.executemany(INSERT_QUERY, batch)
                _connection.commit()
            except Exception:
                print(batch)
            batch = []

    if batch:
        cursor.executemany(INSERT_QUERY, batch)
        _connection.commit()

    cursor.close()


def insert_v2(morphs: Sequence[Tuple[str, str, str]]):
    cursor = _connection.cursor()
    counter = 0
    batch = []
    for morph in morphs:
        batch.append(morph)
        counter += 1
        if len(batch) % BATCH_SIZE == 0:
            try:
                cursor.executemany(INSERT_QUERY_V2, batch)
                _connection.commit()
                print(counter)
            except Exception:
                print(batch)
            batch = []

    if batch:
        cursor.executemany(INSERT_QUERY_V2, batch)
        _connection.commit()

    cursor.close()