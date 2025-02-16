import sqlglot
from sqlglot.errors import ParseError
from sqlglot.expressions import Table, Column

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
        except ParseError as e:
            return {"status": "KO", "message": f"Error de sintaxis: {str(e)}"}

        # Validar tablas en el esquema
        #tables_in_query = parsed.find_all(Table)
        #for table in tables_in_query:
        #    table_name = table.name
        #    if table_name not in self.db_schema:
        #        return {
        #            "status": "KO",
        #            "message": f"The table '{table_name}' does not exist in the schema.",
        #        }

        # Validar columnas
        #columns_in_query = parsed.find_all(Column)
        #for column in columns_in_query:
        #    column_name = column.name
        #    table_name = column.table
        #    if table_name and table_name in self.db_schema:
        #        if column_name not in self.db_schema[table_name]:
        #            return {
        #                "status": "KO",
        #                "message": f"Column '{column_name}' does not exist in table '{table_name}'.",
        #            }

        # Detectar ambigüedades comunes: JOIN sin WHERE → CROSS JOIN implícito   ------------------------------------------------EN DESARROLLO-----------------------------------------
        #if "WHERE" not in sql_query.upper() and "JOIN" in sql_query.upper():
            #return {"status": "ambiguous", "message": ""}

        return {"status": "OK", "message": ""}
