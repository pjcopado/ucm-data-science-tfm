from llm_handler import LLMHandler

class InsightGenerator:
    def __init__(self, model_name="mistral-7b-instruct-v0.2.Q4_K_M"):
        """
        Inicializa el generador de respuestas utilizando LLMHandler con llama.cpp
        """
        self.llm_handler = LLMHandler(model_name=model_name)

    def generate_response(self, user_question, sql_result):
        """
        Genera una respuesta basada en la pregunta del usuario y el resultado SQL.

        Args:
            user_question (str): Pregunta original del usuario.
            sql_result (str | int | float): Resultado de la consulta SQL.

        Returns:
            str: Respuesta generada en lenguaje natural.
        """
        if not user_question.strip():
            return "No se recibió una pregunta válida del usuario."
        if not sql_result:
            return "No se encontraron datos para responder a la consulta."

        prompt = f"""
Pregunta: "{user_question}"
Resultado SQL: {sql_result}
Respuesta esperada:
"""
        
        response = self.llm_handler.generate(prompt)
        return response if response else "No se pudo generar una respuesta válida."

    def close(self):
        """Cierra la instancia de LLMHandler."""
        self.llm_handler.close()


if __name__ == "__main__":
    insight_gen = InsightGenerator()
    user_question = "¿Cuáles fueron las ventas del primer trimestre del 2019 de productos de tela?"
    sql_result = 1900
    response = insight_gen.generate_response(user_question, sql_result)
    print("\n🗨️ **Respuesta Generada:**\n", response)
    insight_gen.close()
