<<<<<<< HEAD:rs-engine/gnn-based/README.md
# Description
A GNN based on GraphSage for learning user and product embeddings.

# Training
To start the training, run the below command:
```bash
python train.py PATH_TO_DATASET_DIR --epochs=[NUM_EPOCHS] --output_dir=[PATH_TO_OUTPUT_DIR]
```
The script assumes the following files exists in `PATH_TO_DATASET_DIR`:
- `users.csv`: A csv file containing all the users.
- `products.csv`: A csv file containing all the products.
- `interactions.csv`: A csv file connecting users to products (purchases).
- `recipes.csv`: A csv file containing all the recipes.
- `products_recipes.csv`: A csv file that connects each product item to a recipe.

The training script output:
- `model.pt`: The trained PyTorch model.
- `user_embedding.csv`: The trained user embedding.
- `product_embedding.csv`: The trained product embedding.

# Evaluation
To evaluate the trained embedding, `generate_recommendations.py` produces a csv file for usage with `evaluate.py` contains in the root of `rs-engine`.

To produce the csv file, run the below command:
```bash
python generate_recommendations.py PATH_TO_DATASET_DIR --epochs=[NUM_EPOCHS] --output_dir=[PATH_TO_OUTPUT_DIR]
```
=======
# Project Description

Backend contains APIs that interact with postgresql database and return values that are later used in the frontend. 

# Requirements
pytest===7.2.1

gunicorn===20.1.0

Flask-Migrate===4.0.4

python-dotenv===1.0.0

psycopg2-binary===2.9.5

Flask-SQLAlchemy===3.0.3

postgreSQL database.

# How to run
1. Make you are located in the backend directory.
2. Start the flask server in debug mode.

```bash
flask --app main --debug run
```
>>>>>>> 0d16c67f11b68b978fd118c5cb4b26aa4ef71a2c:backend/README.md
