import torch
import pandas as pd
import torch_geometric.transforms as T
from torch_geometric.data import HeteroData

def prepare_graph(
    users,
    products,
    recipes,
    interactions,
    products_recipes,
):
  """ Convert dataframes to graph data for Pytorch.

  Args:
  ---
  - `users`: DataFrame
    The users dataframe.
  - `products`: DataFrame
    The products dataframe.
  - `recipes`: DataFrame
    The recipes dataframe.
  - `interactions`: DataFrame
    The interactions dataframe.
  - `products_recipes`: DataFrame
    The products_recipes dataframe.

  Returns:
  ---
  Data
    A Pytorch Geometric data object representing the graph.
  """
  users['index'] = pd.RangeIndex(len(users))
  products['index'] = pd.RangeIndex(len(products))
  recipes['index'] = pd.RangeIndex(len(recipes))


  interactions = pd.merge(interactions, users, left_on="user_id", right_on="user_id", how="left")
  interactions = pd.merge(interactions, products, left_on="product_id", right_on="product_id", how="left")
  interactions = interactions[['index_x', 'index_y', 'count']]

  products_recipes = pd.merge(products_recipes, recipes, left_on="recipe_id", right_on="id", how="left")
  products_recipes = products_recipes.groupby('product_id')['cuisine'].agg(set).to_frame('cuisine').reset_index().explode('cuisine')
  products_recipes = pd.crosstab(index=products_recipes['product_id'], columns=products_recipes['cuisine']).reset_index()
  products_recipes.columns.name = None

  data = HeteroData()
  data['user'].x = torch.from_numpy(users.drop(['user_id', 'index'], axis=1).to_numpy()).float()
  data['user'].id = torch.from_numpy(users['user_id'].to_numpy()).long()
  data['product'].x = torch.from_numpy(products.drop(['product_id', 'index'], axis=1).to_numpy()).float()
  data['product'].id = torch.from_numpy(products['product_id'].to_numpy()).long()

  data['user', 'buys', 'product'].edge_index = torch.from_numpy(interactions[['index_x', 'index_y']].to_numpy().transpose())

  data = T.ToUndirected()(data)
  return data