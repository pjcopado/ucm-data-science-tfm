import time
from uuid import uuid4
from .postgres import Postgres
from .template import PromptTemplate
from .query_manager import QueryManager
from .embedding_manager import EmbeddingManager
from .model_logger import ModelLogger
from .llm_handler import LLMHandler
from .system_logger import Logger
from .check_question import CheckQuestion

logger = Logger("Query Generator")


class SQLQueryGenerator:
    def __init__(self, model_name, db_config, max_attempts=3):
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
        print(f"db_config: {db_config}")
        self.postgres = Postgres(db_config)
        logger.info("Fetching table definitions from the database...")
        self.db_schema = self.postgres.get_db_schema()
        self.db_schema_and_relationships = (
            self.postgres.get_db_schema_and_relationships()
        )
        # Instanciar otros modulos
        self.prompt_template = PromptTemplate(model_name)
        self.query_manager = QueryManager(self.db_schema)
        self.embedder = EmbeddingManager()
        self.model_logger = ModelLogger()

        # Cargar otros params
        self.max_attempts = max_attempts

        self.system_prompt_file = "system_prompt.txt"
        self.user_prompt_file = "user_prompt.txt"
        self.system_error_prompt_file = "system_error_prompt.txt"
        self.user_error_prompt_file = "user_error_prompt.txt"

        # Response status
        self.response_status_ok = "query_completed"
        self.response_status_ko = "query_failed"
        self.response_status_invalid = "query_invalid"

        # Cargar modelo check question
        self.question_checker = CheckQuestion()

        # Cargar el modelo
        system_prompt = str(
            self.prompt_template.generate_prompt(
                "system",
                self.system_prompt_file,
                user_input="",
                user_instructions="",
                db_schema=self.db_schema_and_relationships,
            )
        )
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
        try:
            uuid = uuid4()
            attempts = 0
            errors = []
            initial_query = None

            user_instructions = "" if not user_instructions else user_instructions
            db_schema = self.db_schema_and_relationships if not db_schema else db_schema

            question_checked = self.question_checker.generate_response(user_input)
            if isinstance(question_checked, tuple):
                e, _ = question_checked
                status = self.response_status_ko
                response = {
                    "id": None,
                    "query": None,
                    "confidence_score": None,
                    "status": status,
                }
                logger.error(e)
                return e, response

            if question_checked["status"] == "OK":
                while attempts < self.max_attempts:
                    if not errors:
                        user_input_embedding = self.embedder.embed_text(user_input)
                        similarity_list = self.model_logger.log_similarity_search(
                            user_input_embedding,
                            top_k=3,
                            compare="user_input",
                            status="OK",
                            threshold=0.90,
                        )
                        logger.info(f"similarity_list: {similarity_list}")

                        prompt = self.prompt_template.generate_prompt(
                            "user",
                            self.user_prompt_file,
                            user_input,
                            user_instructions,
                            db_schema,
                            similarity_list=similarity_list,
                        )

                    elif errors and attempts == 1:
                        prompt = self.prompt_template.generate_prompt_combined(
                            "system",
                            self.system_error_prompt_file,
                            "user",
                            self.user_error_prompt_file,
                            user_input,
                            user_instructions,
                            db_schema,
                            error_list=errors,
                            initial_query=initial_query,
                        )

                    else:
                        prompt = self.prompt_template.generate_prompt(
                            "user",
                            self.user_error_prompt_file,
                            user_input,
                            user_instructions,
                            db_schema,
                            error_list=errors,
                            initial_query=initial_query,
                        )

                    # Execute Model
                    start_time = time.time()

                    # Generate query
                    query_text = self.llm.generate(prompt)
                    logger.info(f"Model output: {query_text}")
                    end_time = time.time()
                    execution_time = end_time - start_time
                    query = query_text
                    logger.info(f"Query generated. Execution time: {execution_time}")

                    # Validate query
                    logger.info(f"Validating query: {query}")
                    validation_results = self.query_manager.validate_sql_query(query)

                    if validation_results["status"] == "OK":
                        user_input_embedding = self.embedder.embed_text(user_input)
                        query_embedding = self.embedder.embed_text(query)
                        confidence_score = self.model_logger.log_get_confidence_score(
                            query_embedding, compare="query", threshold=0.90
                        )

                        # Write into log
                        logger.info("Writing into log...")
                        self.model_logger.log_evaluation(
                            uuid,
                            user_input,
                            user_input_embedding,
                            query,
                            query_embedding,
                            execution_time,
                        )

                        status = self.response_status_ok

                        logger.info(f"id: {uuid}")
                        logger.info(f"query: {query}")
                        logger.info(f"confidence_score: {confidence_score}")
                        logger.info(f"status: {status}")

                        response = {
                            "id": uuid,
                            "query": query,
                            "confidence_score": confidence_score,
                            "status": status,
                        }

                        return response

                    elif validation_results["status"] == "KO":
                        initial_query = query
                        errors.append(validation_results["message"])

                    attempts += 1
                    logger.info(f"Retrying... ({attempts}/{self.max_attempts})")

                # "A valid query could not be generated. Can you rephrase the question?"
                status = self.response_status_ko
                response = {
                    "id": uuid,
                    "query": None,
                    "confidence_score": None,
                    "status": status,
                }
                logger.warn(
                    f"Could not generate a valid query after multiple attempts. Status: {status}"
                )
                if errors:
                    logger.error(f"Errors trying generate a SQL query: {errors}")
                return response

            else:
                status = self.response_status_invalid
                response = {
                    "id": uuid,
                    "query": None,
                    "confidence_score": None,
                    "status": status,
                }
                logger.warn(f"Not a valid user question. Status: {status}")
                return response

        except Exception as e:
            status = self.response_status_ko
            response = {
                "id": None,
                "query": None,
                "confidence_score": None,
                "status": status,
            }
            logger.error(e)
            return e, response
