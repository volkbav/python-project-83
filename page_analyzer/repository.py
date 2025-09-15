import psycopg2
from psycopg2.extras import DictCursor

from .validator import normilize_url


class UrlRepository:
    def __init__(self, database_url):
        self.database_url = database_url

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
        query = "SELECT * FROM urls WHERE name = %s"

        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, (name,))
                row = cur.fetchone()
                return dict(row) if row else None
    
    def find_by_id(self, id):
        query = "SELECT * FROM urls WHERE id = %s"

        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, (id,))
                row = cur.fetchone()
                return dict(row) if row else None
  
    def get_all_urls(self):
        query = """SELECT DISTINCT ON (u.id)
                u.id,
                u.name,
                c.created_at,
                c.status_code
            FROM urls AS u
            LEFT JOIN url_checks AS c 
                ON c.url_id = u.id
            ORDER BY u.id DESC
            """
        
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query)
                return [dict(row) for row in cur]

    def save(self, url):
        normilized_url = normilize_url(url['name'])
        exist_name = self.find_by_name(normilized_url)
# тут из функции возвращаю тип flash
        if exist_name:
            url['id'] = exist_name['id']
            return "exist"
        else:
            self._create(url)
            return "success"

    def check_url_save(self, data):
        
        query = """INSERT INTO  url_checks 
                    (url_id,
                    status_code,
                    h1,
                    title,
                    description,
                    created_at) 
                VALUES (%s, %s, %s, %s, %s, NOW())
                RETURNING id"""

        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        data['url_id'],
                        data['status_code'],
                        data['h1'],
                        data['title'],
                        data['description'], 
                    ),
                )
            conn.commit()

    def get_all_checks(self, url_id):
        query = """SELECT * FROM url_checks
            WHERE url_id=%s
            ORDER BY id DESC
            """
        
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, (url_id,))
                return [dict(row) for row in cur]

