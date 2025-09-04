import os

import psycopg2
from psycopg2.extras import DictCursor

DATABASE_URL = os.getenv('DATABASE_URL')
if "localhost" in DATABASE_URL:
    conn = psycopg2.connect(DATABASE_URL)
else:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn
        self._init_schema()

    def _init_schema(self):
        sql_path = os.path.join(os.path.dirname(__file__), "..", "database.sql")
        with open(sql_path, "r") as f:
            sql = f.read()

        # Разделяем на отдельные запросы по точке с запятой
        statements = [s.strip() for s in sql.split(";") if s.strip()]

        with self.conn:
            with self.conn.cursor() as cur:
                for stmt in statements:
                    cur.execute(stmt)

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