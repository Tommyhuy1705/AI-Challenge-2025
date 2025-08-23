from typing import List
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_keywords(query: str) -> List[str]:
    return query.lower().split()[:5]  

def calculate_similarity(vector1: List[float], vector2: List[float]) -> float:
    v1 = np.array(vector1).reshape(1, -1)
    v2 = np.array(vector2).reshape(1, -1)
    return float(cosine_similarity(v1, v2)[0][0])
