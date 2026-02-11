import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
import torch_geometric.transforms as T

parser = argparse.ArgumentParser(
    description='Generate recommendations for usage with evaluate.py.')
parser.add_argument('user', type=str, help='Path to user embedding csv file.')
parser.add_argument('product', type=str,
                    help='Path to product embedding csv file.')
parser.add_argument('--output_path', type=str,
                    help='Path to output path.', default="pred.csv")
args = parser.parse_args()


def read_embedding(filepath):
    """ Read the embedding file.

    Args:
    ---
    - `filepath`: str
        Path to the embedding file.

    Returns:
    Tuple[ndarray, ndarray]
        A tuple in the form of (id, embedding).
    """
    df = pd.read_csv(filepath, header=None)
    return df.loc[:, 0].to_numpy(), df.loc[:, 1:].to_numpy()


if __name__ == "__main__":
    user_ids, user_embedding = read_embedding(args.user)
    prod_ids, product_embedding = read_embedding(args.product)

    # calculate cosine similarity between all users and products
    dot_prod = np.dot(user_embedding, product_embedding.T)
    norm_user = np.linalg.norm(user_embedding, axis=1)
    norm_product = np.linalg.norm(product_embedding, axis=1)
    cosine_sim = dot_prod / np.outer(norm_user, norm_product)

    # sort the result from close
    df = pd.DataFrame(np.concatenate([
        np.expand_dims(user_ids, axis=0).T,
        prod_ids[np.argsort(-1 * cosine_sim, axis=-1)],
    ], axis=1), dtype=np.int32)

    df.to_csv(args.output_path, index=False, header=None)
