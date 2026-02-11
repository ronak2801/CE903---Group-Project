import ast

def preprocess_products(df):
  product_features = [
      'product_id',
      'nutrients.ENERC_KCAL',
      'nutrients.PROCNT',
      'nutrients.FAT',
      'nutrients.CHOCDF',
      'nutrients.FIBTG',
      'health.calories',
      'health.healthLabels'
  ]

  df = df[product_features]

  df['health.healthLabels'] = df['health.healthLabels'].apply(lambda x: ast.literal_eval(x))

  labels = df.explode('health.healthLabels')['health.healthLabels'].unique()

  for val in labels:
      df[val] = df['health.healthLabels'].apply(lambda x: 1 if val in x else 0)

  df = df.drop('health.healthLabels', axis=1)
  df = df.fillna(0)
  return df