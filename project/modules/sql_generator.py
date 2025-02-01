import os
import sys
import re
from sqlglot import ParseError, exp, parse_one

# Set the root directory to import own modules
root_dir = os.path.dirname(os.getcwd())
sys.path.append(root_dir)

from .prompt_loader import PromptLoader  # noqa
from modules.postgres import Postgres  # noqa


class SQLQueryGenerator:
    def __init__(
            self,
            model,
            tokenizer,
            postgres_db: Postgres,
            prompt_loader=None,
            max_attempts=3):
        """
        Inicializa la clase SQLQueryGenerator.

        Args:
            model: Modelo de generación de texto (Hugging Face).
            tokenizer: Tokenizador del modelo.
            prompt_loader (PromptLoader, opcional): Loader para cargar prompts. Si no se proporciona, se debe instanciar manualmente.
            max_attempts (int): Número máximo de intentos para corregir errores.
        """
        self.model = model
        self.tokenizer = tokenizer
        self.postgres_db = postgres_db
        self.db_schema = postgres_db.get_db_schema()
        self.db_prompt_description = postgres_db.get_db_schema_and_relationships()
        self.max_attempts = max_attempts
        self.prompt_loader = prompt_loader or PromptLoader(
            prompt_dir="./prompts"
        )  # Fallback preconfigured

    def validate_sql_query(self, sql_query):
        """
        Valida una consulta SQL utilizando SQLGlot.
        Args:
            sql_query (str): Consulta SQL a validar.
            database_schema (dict): Esquema de la base de datos con tablas y columnas.
        Returns:
            dict: Resultado de la validación con estado ('valid', 'error', 'ambiguous') y mensaje.
        """
        try:
            parsed = parse_one(sql_query)
        except ParseError as e:
            return {"status": "error", "message": f"Error de sintaxis: {str(e)}"}

        """
        # Validar tablas en el esquema
        tables_in_query = parsed.find_all(exp.Table)
        print("tables_in_query")
        print(tables_in_query)
        for table in tables_in_query:
            print("table")
            print(table)
            table_name = table.name
            print("table_name")
            print(table_name)
            if table_name not in self.db_schema:
                return {
                    "status": "error",
                    "message": f"La tabla '{table_name}' no existe en el esquema.",
                }

        # Validar columnas
        columns_in_query = parsed.find_all(exp.Column)
        print("columns_in_query")
        print(columns_in_query)

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
        """

        return {"status": "valid", "message": "La consulta es válida."}

    def extract_sql_query(
            self,
            text: str,
    ):
        """
        Extrae una consulta SQL del prompt en formato Markdown.
        Args:
            text (str): Texto en formato Markdown.
        Returns:
            str: Consulta SQL extraída (o None si no se encuentra).
        """
        match = re.search(r'```sql\n(.*?);', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def generate_sql_query(
        self,
        prompt_file: str,
        retry_prompt_file: str,
        user_input: str,
        instructions: str,
    ):
        """
        Genera una consulta SQL y realiza correcciones automáticas en caso de error.
        Args:
            prompt_file (str): nombre del archivo plantilla del prompt.
            retry_prompt_file (str): nombre del archivo plantilla del prompt de reintento si error.
            user_input (str): Pregunta del usuario.
            instructions (str): Instrucciones adicionales.
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
                    database_schema=self.db_prompt_description,
                )
            else:
                error_section = ""
                for i, error in enumerate(errors, start=1):
                    error_section = f"ERROR {i}:\n{error}\n\n"

                # Load retry prompt
                prompt_content = self.prompt_loader.load_prompt(retry_prompt_file)
                prompt = prompt_content.format(
                    user_question=user_input,
                    instructions=(instructions or "") + error_section,
                    database_schema=self.db_prompt_description,
                    initial_query=initial_query,
                    error_description=error_section,
                )

            # Execute Model
            inputs = self.tokenizer(prompt, return_tensors="pt")

            outputs = self.model.generate(
                **inputs
            )  # params pre-configured in generation_config.json
            print("**********************************************")
            print("outputs")
            print(outputs)

            result = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True)
            print("----------------------------------------------")
            print("result")
            print(result)

            # Extract SQL query from generated text
            sql_query = self.extract_sql_query(result)
            print(f"Consulta generada:\n {sql_query}\n")

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
