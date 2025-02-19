import os
import sys
import dotenv
from .postgres import Postgres

dotenv.load_dotenv()


class ModelLogger:
    def __init__(self):
        """
        Inicializa la clase Logger para manejar los logs de evaluación.
        """
        llm_db_config = {
            "host": os.getenv("LLM_POSTGRES_HOST"),
            "port": os.getenv("LLM_POSTGRES_PORT"),
            "database": os.getenv("LLM_POSTGRES_DB"),
            "user": os.getenv("LLM_POSTGRES_USERNAME"),
            "password": os.getenv("LLM_POSTGRES_PASSWORD"),
        }
        self.evaluation_log = Postgres(llm_db_config)
        print(f"llm_db_config: {llm_db_config}")

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

    def log_evaluation(
        self,
        uuid,
        user_input,
        user_input_embedding,
        query,
        query_embedding,
        execution_time,
    ):
        """
        Registra datos de evaluación de queries.
        """
        user_input_embedding = self._to_vector_format(user_input_embedding)
        query_embedding = self._to_vector_format(query_embedding)
        is_correct = None

        self.evaluation_log.insert_log(
            uuid,
            user_input,
            user_input_embedding,
            query,
            query_embedding,
            is_correct,
            execution_time,
        )

    def user_query_check(self, uuid, is_correct):
        """
        Marca una entrada en el log como correcta o incorrecta.
        Args:
            uuid (str): El UUID del registro a actualizar.
            is_correct (bool): El nuevo valor para el campo is_correct.
        """
        try:
            is_update = self.evaluation_log.update_is_correct(uuid, is_correct)
            if is_update:
                return {"status": "update_completed"}
            else:
                return {"status": "update_failed"}
        except Exception as e:
            return e, {"status": "update_failed"}

    def log_similarity_search(
        self, embedding, top_k=3, compare="user_input", status="OK", threshold=0.0
    ):
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

        return self.evaluation_log.dot_score(
            embedding=embedding,
            top_k=top_k,
            column=column,
            is_correct=is_correct,
            threshold_similarity=threshold,
        )

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
            threshold_freq=threshold,  # Para la freq
        )

        if not result:
            return 0.0

        entry_dict, best_sim = result[0]
        row_freq = entry_dict["freq_above_threshold"]

        # heurística
        score = min(1, best_sim + 0.01 * row_freq)
        return score
