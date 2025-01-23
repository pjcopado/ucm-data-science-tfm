import sqlglot
from sqlglot.errors import ParseError
from modules.postgres import Postgres
from modules.prompt_loader import PromptLoader

class SQLQueryGenerator:
    def __init__(
            self,
            model,
            tokenizer,
            db_config,
            prompt_loader=None,
            max_attempts=3):
        """
        Inicializa la clase SQLQueryGenerator.

        Args:
            model: Modelo de generación de texto (Hugging Face).
            tokenizer: Tokenizador del modelo.
            db_config (dict): Esquema conexión de la base de datos.
            prompt_loader (PromptLoader, opcional): Loader para cargar prompts. Si no se proporciona, se debe instanciar manualmente.
            max_attempts (int): Número máximo de intentos para corregir errores.
        """
        self.model = model
        self.tokenizer = tokenizer
        self.max_attempts = max_attempts
        self.prompt_loader = prompt_loader or PromptLoader(
            prompt_dir="./prompts"
        )  # Fallback preconfigured

        # Instanciar Postgres y cargar el esquema
        self.postgres = Postgres(db_config)
        try:
            self.db_schema = self.postgres.get_db_schema()
        except Exception as e:
            raise RuntimeError(f"Error al cargar el esquema de la base de datos: {e}")

    def validate_sql_query(self, sql_query):
        """
        Valida una consulta SQL utilizando SQLGlot.

        Args:
            sql_query (str): Consulta SQL a validar.

        Returns:
            dict: Resultado de la validación con estado ('valid', 'error', 'ambiguous') y mensaje.
        """
        try:
            parsed = sqlglot.parse_one(sql_query)
        except ParseError as e:
            return {"status": "error", "message": f"Error de sintaxis: {str(e)}"}

        # Validar tablas en el esquema
        tables_in_query = parsed.find_all("Table")
        for table in tables_in_query:
            table_name = table.name
            if table_name not in self.db_schema:
                return {
                    "status": "error",
                    "message": f"La tabla '{table_name}' no existe en el esquema.",
                }

        # Validar columnas
        columns_in_query = parsed.find_all("Column")
        for column in columns_in_query:
            column_name = column.name
            table_name = column.table
            if table_name and table_name in self.db_schema:
                if column_name not in self.db_schema[table_name]:
                    return {
                        "status": "error",
                        "message": f"La columna '{column_name}' no existe en la tabla '{table_name}'.",
                    }

        # Detectar ambigüedades comunes
        if "WHERE" not in sql_query.upper() and "JOIN" in sql_query.upper():
            return {
                "status": "ambiguous",
                "message": "Consulta con JOIN sin un filtro WHERE, podría ser ineficiente.",
            }

        return {"status": "valid", "message": "La consulta es válida."}

    def generate_sql_query(
        self,
        prompt_file: str,
        retry_prompt_file: str,
        user_input: str,
        instructions: str,
        database_schema: str,
    ):
        """
        Genera una consulta SQL y realiza correcciones automáticas en caso de error.
        Args:
            prompt_file (str): nombre del archivo plantilla del prompt.
            retry_prompt_file (str): nombre del archivo plantilla del prompt de reintento si error.
            user_input (str): Pregunta del usuario.
            instructions (str): Instrucciones adicionales.
            database_schema (str): Definiciones de tablas.
        Returns:
            str: Consulta SQL final generada (o None si falla).
        """
        attempts = 0
        errors = []
        initial_query = None

        while attempts < self.max_attempts:
            if not errors:
                prompt_content = self.prompt_loader.load_prompt(prompt_file)
                prompt = prompt_content.format(
                    user_question=user_input,
                    instructions=instructions,
                    database_schema=database_schema,
                )
            else:
                for i, error in enumerate(errors, start=1):
                    error_section = f"ERROR {i}:\n{error}\n\n"
                prompt_content = self.prompt_loader.load_prompt(retry_prompt_file)
                prompt = prompt_content.format(
                    user_question=user_input,
                    instructions=instructions + error_section,
                    database_schema=database_schema,
                    initial_query=initial_query,
                    error_description=error_section,
                )

            # Execute Model
            inputs = self.tokenizer(prompt, return_tensors="pt")

            outputs = self.model.generate(
                **inputs
            )  # params pre-configured in generation_config.json

            sql_query = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True)

            # Validate result
            validation_results = self.validate_sql_query(sql_query)

            if validation_results["status"] == "valid":
                print("Consulta válida generada.")
                return sql_query
            elif validation_results["status"] == "error":
                initial_query = sql_query
                errors.append(validation_results["message"])
                print(f"Error detectado: {validation_results['message']}")
            else:
                print(f"Advertencia: {validation_results['message']}")
                return sql_query

            attempts += 1
            print(f"Reintentando... ({attempts}/{self.max_attempts})")

        print("No se pudo generar una consulta válida tras múltiples intentos.")
        return None
