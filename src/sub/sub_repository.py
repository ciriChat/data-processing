from db.mysql_db import get_connection
from typing import List, Tuple


class SubRepository:
    SAVE_SUB_QUERY = '''
        INSERT INTO subtitle(text, start, stop, hash1, hash2, hash3) VALUES(%s, %s, %s, %s, %s, %s)
    '''

    SAVE_HASH_QUERY = '''
        INSERT INTO tfidf_hash(subtitle_id, hash1, hash2, hash3) VALUES(%s, %s, %s, %s)
    '''

    def __init__(self, conn):
        self.conn = conn

    def save_sub(self, batch: List[Tuple[str, int, int, str, str, str]]):
        cursor = self.conn.cursor()
        cursor.executemany(self.SAVE_SUB_QUERY, batch)
        self.conn.commit()
        cursor.close()

    def save_hash(self, sub_id: int, hash1: str, hash2: str, hash3: str):
        cursor = self.conn.cursor()
        cursor.execute(self.SAVE_HASH_QUERY, (sub_id, hash1, hash2, hash3))
        self.conn.commit()
        cursor.close()


_connection = get_connection('pl_subtitles_db')

sub_repository = SubRepository(_connection)
