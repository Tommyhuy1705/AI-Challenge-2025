from typing import List
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from extract import KeywordExtractor

def get_keywords(query: str) -> List[str]:
    extractor = KeywordExtractor()
    if not query.strip():
        print("Query rỗng")
        return []
    keywords = extractor.extract_keywords(query)
    extractor.release()
    return keywords

def calculate_similarity(vector1: List[float], vector2: List[float]) -> float:
    v1 = np.array(vector1).reshape(1, -1)
    v2 = np.array(vector2).reshape(1, -1)
    return float(cosine_similarity(v1, v2)[0][0])

if __name__ == "__main__":
    query = "A dog is running in the park. Then, it meets a child playing."
    keywords = get_keywords(query)
    print("Keywords:", keywords)
    vec1 = [0.1, 0.2, 0.3]
    vec2 = [0.1, 0.2, 0.4]
    similarity = calculate_similarity(vec1, vec2)
    print("Similarity:", similarity)
    
# Keywords: ['dog running', 'running park', 'child playing', 'park', 'meets child']
# Similarity: 0.9914601339836673