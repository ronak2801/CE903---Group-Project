def preprocess_users(df):
  df = df.drop(['name', 'email'], axis=1)
  return df