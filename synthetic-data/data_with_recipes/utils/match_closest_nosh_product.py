import numpy as np
from gensim.downloader import load

WORD2VEC = load('word2vec-google-news-300')

def match_closest_nosh_product(product, nosh_products):
    """ Match the name of `product` to the closest `non_products` using `WORD2VEC`.
    
    Args:
    ---
    - `product`: str
        The name of the product to match.
    - `nosh_products`: DataFrame
        The nosh product DataFrame

        
    Returns:
    ---
    Dict[str,Any]
        A dictionary with keys `product`, `nosh_product_id`, `nosh_product`, and `similarity`.
    """
    result = []
    
    def __build_product_vector(name):
        v = [WORD2VEC[t] if t in WORD2VEC else np.zeros((WORD2VEC.vector_size,)) for t in name.split(" ")]
        return np.mean(v, axis=0)
    
    for _, row in nosh_products[['product_id', 'product']].iterrows():
        a = __build_product_vector(row['product'].strip())
        b = __build_product_vector(product.strip())
        
        # cosine similarity
        similarity = np.dot(a, b) / ((np.linalg.norm(a) * np.linalg.norm(b)) + 1e-5)
        
        result.append({
            "product": product,
            "nosh_product_id": row['product_id'],
            "nosh_product": row['product'],
            "similarity": similarity
        })
        
    return sorted(result, key=lambda x: x['similarity'], reverse=True)[0]