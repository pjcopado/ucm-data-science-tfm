from llm_handler import LLMHandler  # Importamos el framework de llama.cpp

class InsightGenerator:
    def __init__(self):
        """
        Inicializa el generador de respuestas usando llama.cpp.
        """
        try:
            self.model_name = "flan-t5-xl"
            self.system_prompt = "Eres un asistente experto en análisis de datos."
            
            self.llm = LLMHandler(
                model_name=self.model_name,
                system_prompt=self.system_prompt,
                n_ctx=4096, 
                n_gpu_layers=16, 
                temperature=0.7, 
                top_p=0.9
            )

            print(" Modelo en llama.cpp cargado correctamente.")

        except Exception as e:
            raise RuntimeError(f"Error al cargar el modelo en llama.cpp: {str(e)}")

    def generate_response(self, user_question, sql_result):
        """
        Genera una respuesta en lenguaje humano a partir de la pregunta del usuario y el resultado SQL.

        Args:
            user_question (str): Pregunta original del usuario.
            sql_result (str | int | float): Resultado de la consulta SQL.

        Returns:
            str: Respuesta generada en lenguaje natural y explicativa.
        """
        if not user_question.strip():
            return " No se recibió una pregunta válida del usuario."

        if sql_result is None:
            return " No se encontraron datos para responder a la consulta."

        # 🔹 **Nuevo Prompt Mejorado para llama.cpp**
        prompt = f"""
        Contexto:
        Eres un analista de datos avanzado. Un usuario ha realizado una consulta y tú debes responder de manera clara y precisa.
        
        Ejemplo 1:
        Pregunta: "¿Cuánto vendimos en el sector de moda en enero de 2023?"
        Resultado SQL: 15,340
        Respuesta esperada: "Las ventas en moda durante enero de 2023 fueron de 15,340 unidades. Esto puede estar relacionado con las rebajas de temporada."

        Ejemplo 2:
        Pregunta: "¿Cuál fue la facturación total en alimentos en diciembre de 2022?"
        Resultado SQL: 48,950
        Respuesta esperada: "En diciembre de 2022, la facturación en alimentos alcanzó 48,950 dólares, reflejando un alto consumo por festividades."

        Ahora responde con tu propio razonamiento:
        Pregunta: "{user_question}"
        Resultado SQL: {sql_result}
        Respuesta esperada:
        """

        try:
            response = self.llm.generate(prompt)
            return response.strip() if response else "No se pudo generar una respuesta válida."

        except Exception as e:
            return f" Error al generar la respuesta: {str(e)}"

    def close(self):
        """Cierra el proceso de llama.cpp si sigue en ejecución."""
        self.llm.close()

#  **Ejemplo de Prueba**
if __name__ == "__main__":
    insight_gen = InsightGenerator()

    user_question = "¿Cuales fueron las ventas del primer trimestre del 2019 de productos de tela?"
    sql_result = 1900  # Simulamos la respuesta SQL como una cifra

    response = insight_gen.generate_response(user_question, sql_result)

    print("\n**Respuesta Generada:**\n", response)

    insight_gen.close()
