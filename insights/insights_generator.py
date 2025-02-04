import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class InsightGenerator:
    def __init__(self, model_name="google/flan-t5-xl"):
        """
        Inicializa el generador de respuestas con un modelo optimizado para razonamiento.
        """
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Cargando modelo en {self.device}...")

            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)

            print("Modelo cargado correctamente.")

        except Exception as e:
            raise RuntimeError(f"Error al cargar el modelo: {str(e)}")

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
            return "No se recibió una pregunta válida del usuario."

        if not sql_result:
            return "No se encontraron datos para responder a la consulta."

        # 🔹 **Nuevo Prompt Mejorado para Razonamiento**
        prompt = f"""
Ejemplo 1:
Pregunta: "¿Cuánto vendimos en el sector de moda en enero de 2023?"
Resultado SQL: 15,340
Respuesta esperada: "Las ventas totales en el sector de moda durante enero de 2023 fueron de 15,340 unidades. Enero suele ser un mes con buenas ventas debido a las rebajas de temporada."

Ejemplo 2:
Pregunta: "¿Cuál fue la facturación total en la categoría de alimentos en diciembre de 2022?"
Resultado SQL: 48,950
Respuesta esperada: "En diciembre de 2022, la facturación total en la categoría de alimentos fue de 48,950 dólares. Este mes suele ser alto en ventas debido a la demanda de productos para las festividades."

Ejemplo 3:
Pregunta: "¿Cuántas unidades se vendieron en la categoría de deportes en abril de 2022?"
Resultado SQL: 12,000
Respuesta esperada: "En abril de 2022, la categoría de deportes vendió 12,000 unidades, lo que refleja un alto interés en el equipamiento deportivo con la llegada del buen clima."

Ahora responde la siguiente pregunta de manera similar pero no igual con tu propio razonamiento, razonando el contexto correctamente:
Pregunta: "{user_question}"
Resultado SQL: {sql_result}
Respuesta esperada:
"""

        try:
            # Tokenización
            inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True).to(self.device)

            # 🔹 **Generación Optimizada**
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=150,  # Permite respuestas más largas
                do_sample=True,
                temperature=0.7,  # Más control en la variabilidad
                top_p=0.9,
                num_return_sequences=1
            )

            # Decodificación del texto generado
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

            return response if response else "No se pudo generar una respuesta válida."

        except Exception as e:
            return f"Error al generar la respuesta: {str(e)}"


# 🔥 **Ejemplo de Prueba**
if __name__ == "__main__":
    insight_gen = InsightGenerator()

    # 🔹 **Simulando Pregunta del Usuario y Respuesta SQL**
    user_question = "¿Cuales fueron las ventas del primer trimestre del 2019 de productos de tela?"
    sql_result = 1900  # Simulamos la respuesta SQL como una cifra

    # Generar la respuesta en lenguaje natural y explicativa
    response = insight_gen.generate_response(user_question, sql_result)

    print("\n🗨️ **Respuesta Generada:**\n", response)
