from typing import List, Tuple, Sequence
from db.mysql_db import get_connection

INSERT_QUERY = 'INSERT INTO idf_pl(word, value) VALUES(%s, %s)'
SELECT_QUERY = 'SELECT value FROM idf_pl WHERE word = %s'
BATCH_SIZE = 500

_connection = get_connection('idf_db')


def insert(idfs: Sequence[Tuple[str, float]]):
    cursor = _connection.cursor()

    batch = []
    for idf in idfs:
        batch.append(idf)
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


def find(word: str) -> float:
    cursor = _connection.cursor()
    cursor.execute(SELECT_QUERY, (word,))
    result = float(cursor.fetchone()[0])
    cursor.close()
    return result


def select_all():
    cursor = _connection.cursor()
    cursor.execute("SELECT * FROM idf_pl")
    result = cursor.fetchall()
    cursor.close()
    return result


class CachedIdfRepository:
    def __init__(self):
        self.idfs = dict(select_all())

    def find(self, word: str) -> float:
        return self.idfs[word]



def _chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]



