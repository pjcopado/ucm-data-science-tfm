import torch
from sentence_transformers import SentenceTransformer, util
from .system_logger import Logger

logger = Logger("Embedder")

class EmbeddingManager:
    def __init__(self, model_name="all-MiniLM-L12-v2", device="cuda"):

        if device == "cuda":
            self.device = "cuda" if torch.cuda.is_available() else "auto"
        else:
            self.device = device

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
