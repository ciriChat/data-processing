
from typing import Tuple, Sequence

from db.mysql_db import get_connection

_connection = get_connection('pl_subtitles_db')

BATCH_SIZE = 10000

INSERT_QUERY = '''
    INSERT INTO emotions_pl(word, category, happiness, anger, sadness, fear, disgust) VALUES(%s, %s, %s, %s, %s, %s, %s)
'''


def insert(emotions: Sequence[Tuple[str, str, float, float, float, float, float]]):
    cursor = _connection.cursor()

    batch = []
    for emotion in emotions:
        batch.append(emotion)
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
