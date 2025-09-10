import psycopg2
from psycopg2.extras import DictCursor

from .validator import normilize_url


class UrlRepository:
    def __init__(self, database_url):
        self.database_url = database_url

    def get_content(self):
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM urls")
                return [dict(row) for row in cur]
        
    def _create(self, url):
        normilized_url = normilize_url(url['name'])
        
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO urls (name, created_at) 
                    VALUES (%s, NOW()) RETURNING id""",
                    (normilized_url,),
                )
                id = cur.fetchone()[0]
                url["id"] = id
            conn.commit()

    def find(self, id):
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
                row = cur.fetchone()
                return dict(row) if row else None
    
    def _update(self, url):
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE urls SET name = %s WHERE id = %s",
                    (url["name"], url["id"]),
                )
            conn.commit()

    def get_all(self):
        return self.get_content()
    
    def delete(self, id):
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM urls WHERE id = %s", (id,))
            conn.commit()

    def save(self, url):
        if "id" in url and url["id"]:
            self._update(url)
        else:
            self._create(url)