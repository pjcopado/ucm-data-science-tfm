import psycopg2

class Postgres:
    def __init__(self, db_config):
        """
        Clase para interactuar con la base de datos PostgreSQL.

        Args:
            db_config (dict): Configuración de conexión a la base de datos.
        """
        self.db_config = db_config



    def get_db_schema(self):
        """
        Recupera el esquema de la base de datos y lo transforma en un diccionario.

        Returns:
            dict: Esquema de la base de datos (tablas y columnas).
        """
        schema = {}
        query = """
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    for table_name, column_name in cur.fetchall():
                        if table_name not in schema:
                            schema[table_name] = []
                        schema[table_name].append(column_name)
        except Exception as e:
            raise RuntimeError(f"Error al obtener el esquema de la base de datos: {e}")

        return schema



    def get_db_schema_and_relationships(self):
        """
        Recupera el esquema de las tablas y las relaciones entre ellas.
        
        Returns:
            str: Informe completo del esquema y relaciones.
        """
        schema_details = []
        relationships = []
        
        # Query para obtener el esquema de las tablas
        schema_query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """
        
        # Query para obtener las relaciones (claves foráneas)
        relationships_query = """
        SELECT 
            tc.constraint_name AS fk_name,
            tc.table_name AS source_table,
            kcu.column_name AS source_column,
            ccu.table_name AS target_table,
            ccu.column_name AS target_column
        FROM 
            information_schema.table_constraints AS tc
        JOIN 
            information_schema.key_column_usage AS kcu
        ON 
            tc.constraint_name = kcu.constraint_name
        JOIN 
            information_schema.constraint_column_usage AS ccu
        ON 
            ccu.constraint_name = tc.constraint_name
        WHERE 
            tc.constraint_type = 'FOREIGN KEY'
        ORDER BY 
            source_table, target_table;
        """

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    # Obtener esquema de las tablas
                    cur.execute(schema_query)
                    current_table = None
                    for table_name, column_name, data_type in cur.fetchall():
                        if table_name != current_table:
                            current_table = table_name
                            schema_details.append(f"TABLA: {table_name}")
                        schema_details.append(f"  - {column_name}: {data_type}")

                    # Obtener relaciones entre tablas
                    cur.execute(relationships_query)
                    relationships.append("Relaciones entre tablas (Foreign Keys):")
                    for fk_name, source_table, source_column, target_table, target_column in cur.fetchall():
                        relationships.append(
                            f"  - {fk_name}: {source_table}({source_column}) -> {target_table}({target_column})"
                        )

        except Exception as e:
            raise RuntimeError(f"Error al obtener el esquema y las relaciones: {e}")

        # Crear el informe final
        report = "\n".join(schema_details) + "\n\n" + "\n".join(relationships)
        return report
