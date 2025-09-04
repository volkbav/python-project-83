import os

import psycopg2
from psycopg2.extras import DictCursor

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls")
            return [dict(row) for row in cur]
        
    def validate(self, data, current_id=None):
        pass

    def _create(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO urls (name, created_at) 
                VALUES (%s, NOW()) RETURNING id""",
                (url["name"],),
            )
            id = cur.fetchone()[0]
            url["id"] = id
        self.conn.commit()

    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None
    
    def _update(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE urls SET name = %s WHERE id = %s",
                (url["name"], url["id"]),
            )
        self.conn.commit()

    def get_all(self):
        return self.get_content()
    
    def delete(self, id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM urls WHERE id = %s", (id,))
        self.conn.commit()

    def save(self, url):
        if "id" in url and url["id"]:
            self._update(url)
        else:
            self._create(url)