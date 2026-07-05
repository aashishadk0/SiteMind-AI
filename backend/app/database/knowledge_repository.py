from backend.app.database.database import Database


class KnowledgeRepository:
    def __init__(self):
        self.conn = Database.connect()

    def create_source(self, user_id, name, base_url):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO knowledge_sources(
                user_id, name, base_url, status, progress_message
            )
            VALUES(?,?,?,?,?)
            """,
            (user_id, name, base_url, "queued", "Queued for indexing...")
        )

        self.conn.commit()
        return cursor.lastrowid

    def update_progress(self, source_id, status, message, total_pages=None):
        cursor = self.conn.cursor()

        if total_pages is None:
            cursor.execute(
                """
                UPDATE knowledge_sources
                SET status=?, progress_message=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
                """,
                (status, message, source_id)
            )
        else:
            cursor.execute(
                """
                UPDATE knowledge_sources
                SET status=?, progress_message=?, total_pages=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
                """,
                (status, message, total_pages, source_id)
            )

        self.conn.commit()

    def list_sources(self, user_id):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM knowledge_sources
            WHERE user_id=?
            ORDER BY updated_at DESC, id DESC
            """,
            (int(user_id),)
        )

        return [dict(row) for row in cursor.fetchall()]

    def get_source(self, source_id, user_id):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM knowledge_sources
            WHERE id=? AND user_id=?
            """,
            (int(source_id), int(user_id))
        )

        row = cursor.fetchone()
        return dict(row) if row else None

    def delete_source(self, source_id, user_id):
        cursor = self.conn.cursor()

        cursor.execute(
            """
            DELETE FROM knowledge_sources
            WHERE id=? AND user_id=?
            """,
            (int(source_id), int(user_id))
        )

        self.conn.commit()