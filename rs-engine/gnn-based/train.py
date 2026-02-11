import os
import torch
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import torch.nn.functional as F
import torch_geometric.transforms as T
from torch_geometric.loader.link_neighbor_loader import LinkNeighborLoader

import utils
from model import Model

parser = argparse.ArgumentParser(description='Train a Modified GraphSage model.')
parser.add_argument('data', type=str, help='Path to dataset directory.')
parser.add_argument('--epochs', type=int,
                    help='the number of epochs to train', default=100)
parser.add_argument('--output_dir', type=str,
                    help='Path to output dir.', default="result")
args = parser.parse_args()

if __name__ == "__main__":

    os.makedirs(args.output_dir, exist_ok=True) # create output dir if does not exist.
    
    # build graph data for training
    data = utils.prepare_graph(
        users=utils.preprocess_users(pd.read_csv(os.path.join(args.output_dir, "users.csv"))),
        products=utils.preprocess_products(pd.read_csv(os.path.join(args.output_dir, "products.csv"))),
        recipes=pd.read_csv(os.path.join(args.output_dir, "recipes.csv")),
        interactions=utils.preprocess_interactions(pd.read_csv(os.path.join(args.output_dir, "interactions_train.csv"))),
        products_recipes=pd.read_csv(os.path.join(args.output_dir, "products_recipes.csv"))
    )

    # prepare train/validation splits
    train_data, val_data, _ = T.RandomLinkSplit(
        num_val=0.3,
        num_test=0.0,
        disjoint_train_ratio=0.0,
        neg_sampling_ratio=2,
        add_negative_train_samples=True,
        is_undirected=True,
        edge_types=("user", "buys", "product"),
        rev_edge_types=("product", "rev_buys", "user"),
    )(data)

    # data normalization for training and validation set
    train_data["product"].x = F.normalize(train_data["product"].x, 0, 1)
    train_data["user"].x = F.normalize(train_data["user"].x, 0, 1)
    val_data["product"].x = F.normalize(val_data["product"].x, 0, 1)
    val_data["user"].x = F.normalize(val_data["user"].x, 0, 1)

    # create data loader for batch training and validation
    train_loader = LinkNeighborLoader(
        data=train_data,
        num_neighbors=[20, 10],
        neg_sampling_ratio=2,
        edge_label_index=(("user", "buys", "product"), train_data['user', 'buys', 'product'].edge_label_index),
        edge_label=train_data['user', 'buys', 'product'].edge_label,
        batch_size=128,
        shuffle=True,
        directed=False,
    )

    val_loader = LinkNeighborLoader(
        data=val_data,
        num_neighbors=[20, 10],
        neg_sampling_ratio=2,
        edge_label_index=(("user", "buys", "product"), val_data['user', 'buys', 'product'].edge_label_index),
        edge_label=val_data['user', 'buys', 'product'].edge_label,
        batch_size=128,
        shuffle=True,
        directed=False,
    )

    # initialise the model
    model = Model(102, data.metadata())

    # get the device available for training
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: '{device}'")

    model = model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    @torch.no_grad()
    def test(data):
        model.eval()
        pred = model(data)
        target = data["user", "buys", "product"].edge_label
        loss = F.binary_cross_entropy_with_logits(pred, target)
        return float(loss), pred

    def train(data):
        model.train()
        optimizer.zero_grad()
        pred = model(data)
        target = data["user", "buys", "product"].edge_label
        loss = F.binary_cross_entropy_with_logits(pred, target)
        loss.backward()
        optimizer.step()
        return float(loss), pred

    training_history = []


    for epoch in range(1, args.epochs+1):
        total_train_loss = total_train_example = 0

        for batch in tqdm(train_loader):
            loss, pred = train(batch)
            total_train_loss += float(loss) * pred.numel()
            total_train_example += pred.numel()

        train_loss = total_train_loss / total_train_example

        total_val_loss = total_val_example = 0
        for batch in val_loader:
            loss, pred = test(batch)
            total_val_loss += float(loss) * pred.numel()
            total_val_example += pred.numel()

        val_loss = total_val_loss / total_val_example

        print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}, Val Loss: {val_loss:.4f}\n')

        training_history.append({"epoch": epoch, "loss": loss, "val_loss": val_loss}) # save training metrics for visualisation

    # save the trained model
    torch.save(model, "model.pt")

    # save the trained user and product embeddings.
    model.eval()
    embedding = model(data, embedding=True)
    for embedding_type in ['user', 'product']:
        emb = np.concatenate([
            np.expand_dims(data[embedding_type].id.detach().numpy(), axis=0).T,
            embedding[embedding_type].detach().numpy(),
        ], axis=1)
        pd.DataFrame(emb).to_csv(f"{embedding_type}_embedding.csv", index=False, header=None)

    # save the training loss to csv
    training_history = pd.DataFrame(training_history)
    training_history.to_csv(os.path.join(args.output_dir, "training.csv"), index=False)

    # save training graph
    fig = plt.figure(figsize=(5, 3))
    sns.lineplot(data=training_history, x='epoch', y='loss', label='train')
    sns.lineplot(data=training_history, x='epoch', y='val_loss', label='val')
    plt.legend()
    plt.title("Training")
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.savefig(os.path.join(args.output_dir, "training.png"))
