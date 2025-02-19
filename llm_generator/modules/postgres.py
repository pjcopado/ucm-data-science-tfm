import psycopg2


class Postgres:
    def __init__(self, db_config):
        """
        Clase para interactuar con la base de datos PostgreSQL.

        Args:
            db_config (dict): Configuración de conexión a la base de datos.
        """
        self.db_config = db_config

    def execute_query(self, query):
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    return cur.fetchall()
        except Exception as e:
            raise RuntimeError(f"Error executing query: {query} --> {e}")

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
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

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

    def get_db_schema_dtype(self):
        """
        Recupera el esquema de la base de datos y lo transforma en un diccionario.

        Returns:
            dict: Esquema de la base de datos (tablas y columnas).
        """
        schema = {}
        query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    for table_name, column_name, data_type in cur.fetchall():
                        if table_name not in schema:
                            schema[table_name] = []
                        schema[table_name].append((column_name, data_type))
        except Exception as e:
            raise RuntimeError(f"Error al obtener el esquema de la base de datos: {e}")

        return schema

    def get_db_schema_and_relationships(self):
        """
        Recupera el esquema de las tablas, las relaciones entre ellas y ejemplos de datos.

        Returns:
            str: Informe completo del esquema y relaciones.
        """
        schema_details = []
        relationships = []

        # Query para obtener el esquema de las tablas incluyendo descripciones
        schema_query = """
        SELECT
            c.table_schema,
            c.table_name,
            c.column_name,
            c.data_type,
            pgd.description
        FROM pg_catalog.pg_statio_all_tables as st
        LEFT JOIN pg_catalog.pg_description pgd on (
            pgd.objoid = st.relid
        )
        RIGHT JOIN information_schema.columns c on (
            pgd.objsubid   = c.ordinal_position and
            c.table_schema = st.schemaname and
            c.table_name   = st.relname
        )
        WHERE c.table_schema = 'public'
        ORDER BY c.table_name, c.ordinal_position;
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
                    table_columns = {}

                    # Agrupar columnas por tabla
                    for (
                        table_schema,
                        table_name,
                        column_name,
                        data_type,
                        description,
                    ) in cur.fetchall():
                        table_columns.setdefault(table_name, []).append(
                            (column_name, data_type, description)
                        )

                    # Obtener ejemplos de datos por tabla y generar detalles del esquema
                    schema_details = []
                    for table_name, columns in table_columns.items():
                        schema_details.append(f"TABLE: {table_name}")
                        column_names = ", ".join(col[0] for col in columns)
                        cur.execute(f"SELECT {column_names} FROM {table_name} LIMIT 1;")
                        result = cur.fetchone()

                        for i, (column_name, data_type, description) in enumerate(
                            columns
                        ):
                            example = f", example '{result[i]}'" if result else ""
                            schema_details.append(
                                f"  - {column_name}: {data_type}{example}"
                                + (
                                    f" - Column description: {description}"
                                    if description
                                    else ""
                                )
                            )

                    # Obtener relaciones entre tablas
                    cur.execute(relationships_query)
                    fk_results = cur.fetchall()

                    if fk_results:
                        relationships.append(
                            "Relationships between tables (Foreign Keys):"
                        )

                        seen_relationships = set()  # Conjunto para evitar duplicados
                        for (
                            fk_name,
                            source_table,
                            source_column,
                            target_table,
                            target_column,
                        ) in fk_results:
                            relationship_str = f"  - {fk_name}: {source_table}({source_column}) -> {target_table}({target_column})"

                            if relationship_str not in seen_relationships:
                                relationships.append(relationship_str)
                                seen_relationships.add(
                                    relationship_str
                                )  # Agregar al conjunto para evitar duplicados

        except Exception as e:
            raise RuntimeError(f"Error al obtener el esquema y las relaciones: {e}")

        # Crear el informe final
        if relationships:
            report = "\n".join(schema_details) + "\n\n" + "\n".join(relationships)
        else:
            report = "\n".join(schema_details)
        return report

    def insert_log(
        self,
        uuid,
        user_input,
        user_input_embedding,
        generated_query,
        generated_query_embedding,
        is_correct,
        execution_time,
    ):
        query = """
            INSERT INTO logs (uuid, user_input, user_input_embedding, query, query_embedding, is_correct, execution_time, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """

        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    data = (
                        uuid,
                        user_input,
                        user_input_embedding,
                        generated_query,
                        generated_query_embedding,
                        is_correct,
                        execution_time,
                    )
                    cur.execute(query, data)

        except Exception as e:
            raise RuntimeError(f"Error writing evaluation logs: {e}")

    def update_is_correct(self, uuid, is_correct):
        """
        Actualiza el campo is_correct basado en el uuid.
        Args:
            uuid (str): El UUID del registro a actualizar.
            is_correct (bool): El nuevo valor para el campo is_correct.
        """
        query = """
            UPDATE logs
            SET is_correct = %s
            WHERE uuid = %s
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (is_correct, uuid))
        except Exception as e:
            raise RuntimeError(f"Error updating is_correct: {e}")

    def dot_score(
        self,
        embedding,
        top_k=3,
        column="user_input_embedding",
        is_correct=None,
        threshold_similarity=None,
        threshold_freq=0.0,
    ):
        """
        Returns a list of rows ordered by similarity (dot product).

        Params:
          - embedding (list[float]): el vector de búsqueda en formato lista.
          - top_k (int): cuántas filas devolver, ordenadas desc por similitud.
          - column (str): columna de tipo vector (pgvector) contra la que comparar.
          - is_correct (bool | None): si se especifica, filtra 'is_correct = True/False'.
          - threshold (float): umbral para contar cuántas filas superan la similitud
            en la ventana. Si no necesitas 'freq_above_threshold', puedes poner 0.

        Return: List[ (entry_dict, similarity) ]

            entry_dict = {
                "id": ...,
                "user_input": ...,
                "query": ...,
                "is_correct": ...,
                "embedding": ...,
                "freq_above_threshold": ...
            },
            similarity = float()
        """
        if threshold_similarity:
            threshold_freq = threshold_similarity
        else:
            threshold_similarity = 0

        params = {
            "embedding": embedding,
            "threshold_similarity": threshold_similarity,
            "threshold_freq": threshold_freq,
            "top_k": top_k,
            "is_correct": is_correct,
        }

        sub_select = f"""
            SELECT
                id,
                user_input,
                query,
                is_correct,
                {column},
                ABS({column} <#> %(embedding)s::vector) AS similarity
            FROM logs
        """

        where_clause = (
            "similarity > %(threshold_similarity)s AND is_correct = %(is_correct)s"
            if is_correct is not None
            else "similarity > %(threshold_similarity)s"
        )

        final_query = f"""
            SELECT
                id,
                user_input,
                query,
                is_correct,
                {column},
                similarity,
                SUM(
                    CASE WHEN similarity > %(threshold_freq)s THEN 1 ELSE 0 END
                ) OVER () AS freq_above_threshold
            FROM (
                {sub_select}
            ) AS sub
            WHERE {where_clause}
            ORDER BY similarity DESC
            LIMIT %(top_k)s
        """

        results = []
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute(final_query, params)
                    rows = cur.fetchall()
                    for row in rows:
                        row_id = row[0]
                        row_user_input = row[1]
                        row_query = row[2]
                        row_is_correct = row[3]
                        row_embedding = row[4]
                        row_similarity = row[5]
                        row_freq = row[6]

                        # Creamos el diccionario:
                        entry_dict = {
                            "id": row_id,
                            "user_input": row_user_input,
                            "query": row_query,
                            "is_correct": row_is_correct,
                            "embedding": row_embedding,
                            "freq_above_threshold": int(row_freq),
                        }
                        # Retornamos tupla (entry_dict, similarity)
                        results.append((entry_dict, float(row_similarity)))
        except Exception as e:
            raise RuntimeError(f"Error in dot_score: {e}")

        return results
