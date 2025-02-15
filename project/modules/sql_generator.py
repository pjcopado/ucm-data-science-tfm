import time
from modules.postgres import Postgres
from modules.template import PromptTemplate
from modules.query_manager import QueryManager
from modules.embedding_manager import EmbeddingManager
from modules.model_logger import ModelLogger
from modules.llm_handler import LLMHandler
from modules.system_logger import Logger

logger = Logger("Query Generator")

class SQLQueryGenerator:
    def __init__(
            self,
            model_name,
            db_config,
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
        
        # Instanciar Postgres y cargar el esquema
        self.postgres = Postgres(db_config)
        logger.info("Fetching table definitions from the database...")
        self.db_schema = self.postgres.get_db_schema()
        self.db_schema_and_relationships = self.postgres.get_db_schema_and_relationships()
        
        # Instanciar otros modulos
        self.prompt_template = PromptTemplate(model_name)
        self.query_manager = QueryManager(self.db_schema)
        self.embedder = EmbeddingManager()
        self.model_logger = ModelLogger()

        # Cargar otros params
        self.model_dir = f"./models/{model_name}"
        self.max_attempts = max_attempts

        self.system_prompt_file = "system_prompt.txt"
        self.user_prompt_file = "user_prompt.txt"
        self.system_error_prompt_file = "system_error_prompt.txt"
        self.user_error_prompt_file = "user_error_prompt.txt"

        # Cargar el modelo
        system_prompt = str(self.prompt_template.generate_prompt("system", self.system_prompt_file, user_input="", user_instructions="", db_schema=self.db_schema_and_relationships))
        self.llm = LLMHandler(model_name, system_prompt)



    def generate_sql_query(self, user_input, user_instructions=None, db_schema=None):
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

        user_instructions = "" if not user_instructions else user_instructions
        db_schema = self.db_schema_and_relationships if not db_schema else db_schema

        while attempts < self.max_attempts:
            if not errors:
                user_input_embedding = self.embedder.embed_text(user_input)
                similarity_list = self.model_logger.log_similarity_search(user_input_embedding, top_k=3, compare="user_input", status="OK", threshold=0.90)
                print(similarity_list)
                prompt = self.prompt_template.generate_prompt("user", self.user_prompt_file, user_input, user_instructions, db_schema, similarity_list=similarity_list)

            elif errors and attempts == 1:
                prompt = self.prompt_template.generate_prompt_combined("system", self.system_error_prompt_file, "user", self.user_error_prompt_file, user_input, user_instructions, db_schema, error_list=errors, initial_query=initial_query)

            else:
                prompt = self.prompt_template.generate_prompt("user", self.user_error_prompt_file, user_input, user_instructions, db_schema, error_list=errors, initial_query=initial_query)

            # Execute Model
            start_time = time.time()

            query_text = self.llm.generate(prompt)

            logger.info(f"Model output: {query_text}")
            
            #pattern = r"<\|start_header_id\|>assistant<\|end_header_id\|>\s*(.*?)\s*<\|eot_id\|>"
            #match = re.search(pattern, query_text, re.DOTALL)
            #query = match.group(1).strip()
            
            end_time = time.time()
            execution_time = end_time - start_time

            query=query_text
            return query

            validation_results = self.query_manager.validate_sql_query(query)

            if validation_results["status"] == "OK":
                user_input_embedding = self.embedder.embed_text(user_input)
                query_embedding = self.embedder.embed_text(query)
                confidence_score = self.model_logger.log_get_confidence_score(query_embedding, compare="query", threshold=0.85)

                self.model_logger.log_evaluation(user_input, user_input_embedding, query, query_embedding, validation_results, execution_time)

                logger.info("Query validate")
                return query, confidence_score
            
            elif validation_results["status"] == "KO":
                initial_query = query
                errors.append(validation_results["message"])
                user_input_embedding = self.embedder.embed_text(user_input)
                query_embedding = self.embedder.embed_text(query)

                self.model_logger.log_evaluation(user_input, user_input_embedding, query, query_embedding, validation_results, execution_time)
                logger.warn(f"Error detectado: {validation_results['message']}")

            attempts += 1
            logger.info(f"Retrying... ({attempts}/{self.max_attempts})")

        logger.warn("No se pudo generar una consulta válida tras múltiples intentos.")
        query = "A valid query could not be generated. Can you rephrase the question?"
        return query, 0.0
