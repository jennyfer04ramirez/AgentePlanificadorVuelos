from app.embeddings.model import embedding_model
from app.functions.repository import get_top_functions

def select_function(query: str, top_k: int = 3):
    query_embedding = embedding_model.embed_query(query)
    return get_top_functions(query_embedding, top_k)
