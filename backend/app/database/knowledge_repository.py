from backend.app.database.database import Database


class KnowledgeRepository:
    def __init__(self):
        self.conn = Database.connect()

    def create_source(self, name, base_url, status="indexing"):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO knowledge_sources(name, base_url, status)
            VALUES(?,?,?)
            """,
            (name, base_url, status)
        )

        self.conn.commit()

        cursor.execute(
            "SELECT * FROM knowledge_sources WHERE base_url=?",
            (base_url,)
        )

        return dict(cursor.fetchone())

    def update_source(self, source_id, status, total_pages=0):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            UPDATE knowledge_sources
            SET status=?, total_pages=?
            WHERE id=?
            """,
            (status, total_pages, source_id)
        )

        self.conn.commit()

    def list_sources(self):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM knowledge_sources
            ORDER BY created_at DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    def get_source(self, source_id):
        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT * FROM knowledge_sources WHERE id=?",
            (source_id,)
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    def delete_source(self, source_id):
        cursor = self.conn.cursor()

        cursor.execute(
            "DELETE FROM knowledge_sources WHERE id=?",
            (source_id,)
        )

        self.conn.commit()