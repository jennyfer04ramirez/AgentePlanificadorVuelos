# app/utils/similarity.py

import numpy as np


def cosine_similarity(vec1, vec2) -> float:
    """
    Calcula la similitud coseno entre dos vectores.
    Retorna un valor entre -1 y 1.
    """

    v1 = np.array(vec1, dtype=np.float32)
    v2 = np.array(vec2, dtype=np.float32)

    if v1.shape != v2.shape:
        raise ValueError(
            f"Vector size mismatch: {v1.shape} vs {v2.shape}"
        )

    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)

    if norm_v1 == 0.0 or norm_v2 == 0.0:
        return 0.0

    return float(np.dot(v1, v2) / (norm_v1 * norm_v2))
