
from app.embeddings.model import embedding_model
from app.utils.similarity import cosine_similarity

INTENT_TEXTS = {
    "DOMAIN_FLIGHT": (
        "buscar vuelos reservar vuelo precio de vuelo "
        "horarios de vuelo viajar en avion aerolinea"
    ),
    "SOCIAL": (
        "hola buenas gracias chao adios hasta luego"
    ),
    "OUT_OF_DOMAIN": (
        "futbol politica noticias musica campeon del mundo "
    )
}

# Se generan UNA sola vez al cargar el módulo
INTENT_EMBEDDINGS = {
    intent: embedding_model.embed_query(text)
    for intent, text in INTENT_TEXTS.items()
}

def detect_high_level_intent(query: str):
    query_embedding = embedding_model.embed_query(query)

    scores = {
        intent: cosine_similarity(query_embedding, emb)
        for intent, emb in INTENT_EMBEDDINGS.items()
    }

    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]

    return best_intent, best_score
