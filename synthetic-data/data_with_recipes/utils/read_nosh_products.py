import pandas as pd


def read_nosh_products(filepath):
    """ Read nosh product data.

    Args:
    ---
    - `filepath`: str
        The path to nosh product file.

    Returns:
    ---
    DataFrame
        The product data file in pandas DataFrame format.
    """
    df = pd.read_excel(filepath)
    # drop duplicate 'onion', 'peanut', 'cooked rice'
    for i in [74, 115, 167]:
        df = df[df['product_id'] != i]
    return df.reset_index(drop=True)
