import pandas as pd
from datetime import datetime


def read_opensource_purchases(filepath):
    """ Read opensource purchases data with non food transactions removed.

    Args:
    ---
    - `filepath`: str
        The path to the opensource purchases file.

    Return:
    ---
    DataFrame

    """
    non_food_products = [
        'abrasive cleaner', 'baby cosmetics', 'bags',
        'bathroom cleaner', 'candles', 'cleaner',
        'cling film', 'cookware', 'decalcifier',
        'dental care', 'detergent', 'dish cleaner', 'female sanitary products',
        'fertilizer', 'film', 'finished products',
        'hair spray', 'house keeping products', 'hygiene articles',
        'light bulbs', 'make up remover', 'male cosmetics',
        'napkins', 'newspapers', 'pet care', 'preservation products',
        'photo', 'pot plants', 'rubbing alcohol',
        'shopping bags', 'skin care', 'soap',
        'softener', 'toilet cleaner',
        'kitchen towels', 'kitchen utensil',
        'roll products ',
    ]

    # read file and parse date to the d-m-y format
    df = pd.read_csv(
        filepath,
        parse_dates=['Date'],
        date_parser=lambda x: datetime.strptime(x, '%d-%m-%Y')
    )

    # convert purchase sequence to list of string
    df['itemDescription'] = df['itemDescription'].str.split('/')
    df = df.explode('itemDescription')

    # remove non food purchases
    df = df[~df['itemDescription'].isin(non_food_products)]

    df = df.sort_values(by='Member_number')\
        .rename(columns={"Member_number": "customer_id", "itemDescription": "product_name", "Date": "timestamp"})
    df['timestamp'] = df['timestamp'].dt.tz_localize(None)
    return df[['customer_id', 'product_name', 'timestamp']]
