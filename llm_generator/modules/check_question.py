import re
from .system_logger import Logger
from .llm_handler import LLMHandler
from .template import PromptTemplate

logger = Logger("Check Question")


class CheckQuestion:
    def __init__(self, db_schema, model_name="llama-3-sqlcoder-8b-Q8_0"):
        """
        Inicializa el generador de respuestas utilizando LLMHandler con llama.cpp
        """
        # Instanciar otros modulos
        self.prompt_template = PromptTemplate(model_name)

        # Cargar otros params
        self.system_prompt_file = "system_prompt-check_question.txt"
        self.user_prompt_file = "user_prompt-check_question.txt"

        # Cargar el modelo
        system_prompt = str(
            self.prompt_template.generate_prompt("system", self.system_prompt_file, db_schema=db_schema)
        )
        self.llm_handler = LLMHandler(model_name, system_prompt)

    def generate_response(self, user_input):
        """
        Genera una respuesta basada en la pregunta del usuario y el resultado SQL.

        Args:
            user_question (str): Pregunta original del usuario.
            sql_result (str | int | float): Resultado de la consulta SQL.
            query_generate (str): Query generada por el modelo.

        Returns:
            str: Respuesta generada en lenguaje natural.
        """
        try:
            prompt = self.prompt_template.generate_prompt(
                "user", self.user_prompt_file, user_input=user_input
            )

            response = self.llm_handler.generate(prompt)

            # Expresión regular flexible
            logger.debug("Extracting checking question status from model output...")
            rexpr = r"^\s*Answer\s*:?\s*"
            answer = re.sub(rexpr, "", response).strip()

            logger.info(f"Check question status: {answer}")

            response = {"status": answer}

            return response

        except Exception as e:
            response = {
                "status": "KO",
            }
            logger.error(e)
            return e, response

    def close(self):
        """Cierra la instancia de LLMHandler."""
        self.llm_handler.close()
