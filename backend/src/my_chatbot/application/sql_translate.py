from domain.repository.query import query_repository
from domain.repository.sql_translate import translate_repository

# Aplicación
class SqlTranslationService:
    def __init__(self, translator: translate_repository, executor: query_repository):
        self.translator = translator
        self.executor = executor

    def process_text_and_execute(self, text: str) -> None:
        sql_query = self.translator.translate(text)
        self.executor.return_query(sql_query)