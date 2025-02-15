import logging
import json
from modules.postgres import Postgres

class Logger:
    def __init__(self):
        """
        Inicializa la clase Logger para manejar los logs de la aplicación y la evaluación.

        Args:
            app_log_file (str): Archivo para los logs de control de la aplicación.
            evaluation_log_file (str): Archivo para los logs de evaluación de queries.
        """
        self.app_log_file = "app.log"
        self.evaluation_log = Postgres({
            "host": "192.168.1.141",
            "port": 5433,
            "database": "evaluation_log",
            "user": "postgres",
            "password": "postgres"
        })

        # Configurar logging para la aplicación
        logging.basicConfig(
            filename=self.app_log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )



    def _to_vector_format(self, emb):
        """
        Converts the embedding to a databse vector compatible format.
        - Suppresses dimension 0 if the tensor has size (1, dim).
        - Converts the tensor or array to a list of floats.
        - Formats the list as a string '[val1, val2, ...]'.

        Args:
            emb: A tensor, array, or list that represents the embedding.

        Return:
            str: Embedding formatted as '[val1, val2, ...]'.
        """
        # Elimina dimensión adicional si existe
        if hasattr(emb, "dim") and emb.dim() > 1:
            emb = emb.squeeze(0)
        
        # Convierte a lista de floats si es tensor
        if hasattr(emb, "tolist"):
            emb = emb.tolist()

        # Asegura que sea una lista válida
        if not isinstance(emb, list):
            raise ValueError("El embedding debe ser convertible a una lista.")

        # Convierte la lista a formato pgvector
        return f"[{','.join(map(str, emb))}]"




    def log_app_event(self, level, message):
        """
        Registra eventos generales de la aplicación en el archivo de logs de la aplicación.

        Args:
            level (str): Nivel de log (INFO, WARNING, ERROR).
            message (str): Mensaje del evento.
        """
        if level.upper() == "INFO":
            logging.info(message)
        elif level.upper() == "WARNING":
            logging.warning(message)
        elif level.upper() == "ERROR":
            logging.error(message)
        else:
            logging.debug(message)



    def log_evaluation(self, user_input, user_input_embedding, query, query_embedding, validation_results, execution_time):
        """
        Registra datos de evaluación de queries.
        """
        user_input_embedding = self._to_vector_format(user_input_embedding)
        query_embedding = self._to_vector_format(query_embedding)
        
        if validation_results["status"] == "OK":
            is_correct = True
        elif validation_results["status"] == "KO":
            is_correct = False

        self.evaluation_log.insert_log(user_input, user_input_embedding, query, query_embedding, is_correct, validation_results["message"], execution_time)



    def log_similarity_search(self, embedding, top_k=3, compare="user_input", status="OK", threshold=0.0):
        """
        Hola
        """
        embedding = self._to_vector_format(embedding)

        if status == "OK":
            is_correct = True
        elif status == "KO":
            is_correct = False
        else:
            is_correct = None

        if compare == "user_input":
            column = "user_input_embedding"
        else:  # compare == "query"
            column = "query_embedding"
        
        return self.evaluation_log.dot_score(embedding=embedding, top_k=top_k, column=column, is_correct=is_correct, threshold_similarity=threshold)
    


    def log_get_confidence_score(self, embedding, compare="query", threshold=0.0):
        """
        Ejemplo: Pedimos top_k=1, is_correct=True,
        y luego combinamos 'similarity' y 'freq_above_threshold' en una métrica.
        """
        embedding = self._to_vector_format(embedding)

        if compare == "user_input":
            column = "user_input_embedding"
        else:  # compare == "query"
            column = "query_embedding"

        # Pide solo la fila más similar (top_k=1), filtra is_correct=True
        # y define un threshold para el recuento freq_above_threshold
        result = self.evaluation_log.dot_score(
            embedding=embedding,
            top_k=1,
            column=column,
            is_correct=True,
            threshold_freq=threshold  # Para la freq
        )

        if not result:
            return 0.0

        entry_dict, best_sim = result[0]
        row_freq = entry_dict["freq_above_threshold"]

        # heurística
        score = min(1, best_sim + 0.01 * row_freq)
        return score
