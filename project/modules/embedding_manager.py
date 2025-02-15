import torch
from sentence_transformers import SentenceTransformer, util
from modules.system_logger import Logger

logger = Logger("Embedder")

class EmbeddingManager:
    def __init__(self, model_name="all-MiniLM-L12-v2", device="cpu"):

        if device:
            self.device = device 
        else:
            self.device = "cuda" if torch.cuda.is_available() else "auto"
        
        self.model = SentenceTransformer(model_name, device=self.device)
    

    def embed_text(self, text):
        """
        Genera el embedding de un texto (sea la pregunta o la query SQL) 
        usando sentence-transformers.
        - Retorna un tensor en self.device.
        - Normaliza el embedding.
        """
        if not text or not isinstance(text, str):
            # Por si llega un texto vacío o algo no esperado
            # Retorna un embedding de ceros
            emb_dim = self.model.get_sentence_embedding_dimension()
            return torch.zeros(emb_dim, device=self.device)

        embedding = self.model.encode(text, convert_to_tensor=True, normalize_embeddings=True)
        return embedding


    
    
    
    
    
    # -------------------------DEPRECATED----------------------------------------------
    
    def similarity_search(self, query, query_logs, top_k=3, compare="user_input"):
        """
        Devuelve las top_k interacciones más similares a 'query' según 
        la similitud de embeddings.

        compare: "user_input" o "query"
          - "user_input": comparamos contra los embeddings de las preguntas de usuario
          - "query": comparamos contra los embeddings de las consultas SQL

        Retorna lista de tuplas (entry, similitud),
        donde 'entry' es el diccionario guardado en self.query_logs.

        Ejemplo de uso:
          - similarity_search("What was sold yesterday in Spain?", compare="user_input")
          - similarity_search("SELECT * FROM sales", compare="query")
        """
        if not query_logs:
            return []

        new_emb = self.embed_text(query).unsqueeze(0)  # shape: (1, dim)

        if compare == "user_input":
            corpus_embeddings = [x["user_input_embedding"] for x in query_logs]
        else:  # compare == "query"
            corpus_embeddings = [x["query_embedding"] for x in query_logs]

        corpus_tensor = torch.cat(corpus_embeddings, dim=0)  # shape (N, dim)

        scores = util.dot_score(new_emb, corpus_tensor)[0]   # dot_score => shape(1, N)
        top_scores, top_indices = torch.topk(scores, k=min(top_k, len(scores)))

        results = []
        for score, idx in zip(top_scores, top_indices):
            idx = int(idx)
            sim = float(score)
            entry = query_logs[idx]
            results.append((entry, sim))

        return results

    def get_confidence_score(self, query, query_logs, compare="user_input"):
        """
        Devuelve un 'score' de confianza basado en la similitud
        con interacciones anteriores que hayan tenido estado 'valid'.
        Heurística simple: se queda con el valor más alto de dot_score
        frente a las entradas 'valid'.

        compare: "user_input" o "query"
          - Indica si comparamos el nuevo texto con el user_input_embedding
            o con el query_embedding de logs (con status=valid).
        """
        # Filtramos solo las entradas valid
        valid_logs = [x for x in query_logs if x["validation_status"] == "valid"]
        if not valid_logs:
            return 0.0

        new_emb = self.embed_text(query).unsqueeze(0)  # (1, dim)

        if compare == "user_input":
            valid_embeddings = [x["user_input_embedding"] for x in valid_logs]
        else:
            valid_embeddings = [x["query_embedding"] for x in valid_logs]

        valid_tensor = torch.cat(valid_embeddings, dim=0)  # (M, dim)

        # dot_score => shape (1, M)
        scores = util.dot_score(new_emb, valid_tensor)[0]  # (M,)
        best_score = float(torch.max(scores))
        return best_score
