import pandas as pd

def preprocess_interactions(df):
  df = df.groupby(['user_id', 'product_id'])['product_id']\
        .count()\
        .to_frame('count')\
        .reset_index()
  return df