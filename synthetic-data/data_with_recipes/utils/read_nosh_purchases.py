import pandas as pd


def read_nosh_purchases(filepath):
    """ Read Nosh purhcase excel file to Pandas Dataframe.

    Args:
    ---
    - `filepath`: str
        Path to the nosh purchases file.

    Return:
    ---
    Dataframe
        Nosh purchases data in Pandas Dataframe format.
    """
    df = pd.read_excel(filepath, parse_dates=['purchase_date_time'])\
        .drop(['invoice_id', 'customer_name'], axis=1)\
        .rename(columns={"product_id_purchased": "product_id", "purchase_date_time": "timestamp"})

    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    df['timestamp'] = df['timestamp'].dt.normalize()
    return df
