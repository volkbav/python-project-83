import psycopg2
from psycopg2.extras import DictCursor

from .validator import normilize_url


class UrlRepository:
    def __init__(self, database_url):
        self.database_url = database_url

    def get_content(self):
        query = """SELECT * FROM urls
            ORDER BY id DESC"""
        
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query)
                return [dict(row) for row in cur]
        
    def _create(self, url):
        normilized_url = normilize_url(url['name'])
        query = """INSERT INTO urls (name, created_at) 
            VALUES (%s, NOW()) RETURNING id"""

        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    (normilized_url,),
                )
                id = cur.fetchone()[0]
                url["id"] = id
            conn.commit()

    def find_by_name(self, name):
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE name = %s", (name,))
                row = cur.fetchone()
                return dict(row) if row else None
    
    def get_all(self):
        return self.get_content()
    
    def delete(self, id):
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM urls WHERE id = %s", (id,))
            conn.commit()

    def save(self, url):
        normilized_url = normilize_url(url['name'])
        exist_name = self.find_by_name(normilized_url)
        if exist_name:
            url['id'] = exist_name['id']
            return exist_name
        else:
            self._create(url)
            return url

    