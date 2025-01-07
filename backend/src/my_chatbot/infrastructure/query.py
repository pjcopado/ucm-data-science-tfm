from my_chatbot.domain.repository.query import query_repository

class PostgresDatabaseExecutor(query_repository):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def return_query(self, query: str) -> list:
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return results