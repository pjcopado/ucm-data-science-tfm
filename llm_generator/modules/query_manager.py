import sqlglot
from sqlglot.errors import ParseError
from system_logger import Logger

logger = Logger("Query Manager")


class QueryManager:
    def __init__(self, db_schema):
        """
        db_schema: diccionario de la forma:
        {
            "tabla1": ["col1", "col2", ...],
            "tabla2": ["colA", "colB", ...],
            ...
        }
        """
        self.db_schema = db_schema

    def validate_sql_query(self, sql_query):
        """
        Validate SQL query sintaxis.

        Return:
          - status: 'OK' | 'KO' | 'ambiguous'
          - message: error
        """
        try:
            sqlglot.parse_one(sql_query)
            return {"status": "OK", "message": ""}

        except ParseError as e:
            logger.warn(f"Error de sintaxis: {str(e)}")
            return {"status": "KO", "message": f"Error de sintaxis: {str(e)}"}
