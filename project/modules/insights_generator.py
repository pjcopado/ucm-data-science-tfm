import re
from modules.system_logger import Logger
from modules.llm_handler import LLMHandler
from modules.template import PromptTemplate

logger = Logger("Insights Generator")


class InsightGenerator:
    def __init__(self, model_name="llama-3_2-3B-instruct-Q6_K_L"):
        """
        Inicializa el generador de respuestas utilizando LLMHandler con llama.cpp
        """
        # Instanciar otros modulos
        self.prompt_template = PromptTemplate(model_name)

        # Cargar otros params
        self.system_prompt_file = "system_prompt.txt"
        self.user_prompt_file = "user_prompt.txt"

        # Cargar el modelo
        system_prompt = str(
            self.prompt_template.generate_prompt("system", self.system_prompt_file)
        )
        self.llm_handler = LLMHandler(model_name, system_prompt)

    def generate_response(self, user_input, query_result, query_generated):
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
            if not user_input:
                return "No se recibió una pregunta válida del usuario."
            if not query_result:
                return "No se encontraron datos para responder a la consulta."

            prompt = self.prompt_template.generate_prompt(
                "user",
                self.user_prompt_file,
                user_input=user_input,
                query_result=query_result,
                query_generated=query_generated,
            )

            response = self.llm_handler.generate(prompt)

            # Expresión regular flexible
            logger.debug("Extracting answer and explanation from model output...")
            rexpr = r"(?:\*\*)?\s*Answer\s*(?:\*\*)?\s*:?\s*|\s*(?:\*\*)?Explanation\s*(?:\*\*)?\s*:?\s*"
            parts = re.split(rexpr, response)
            parts = [p for p in parts if p.strip()]

            answer = re.sub(r"\*\*", "", parts[0]).strip() if len(parts) > 0 else ""
            explanation = (
                re.sub(r"\*\*", "", parts[1]).strip() if len(parts) > 1 else ""
            )
            status = "insight_completed"

            logger.info(f"insights_reponse: {answer}")
            logger.info(f"query_explanation: {explanation}")
            logger.info(f"status: {status}")

            response = {
                "insights_reponse": answer,
                "query_explanation": explanation,
                "status": status,
            }

            return response

        except Exception as e:
            status = "insight_failed"
            response = {"status": status}
            logger.error(e)
            return e, response

    def close(self):
        """Cierra la instancia de LLMHandler."""
        self.llm_handler.close()
