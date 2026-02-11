import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv, to_hetero, GraphSAGE

class GNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), hidden_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

class Classifier(torch.nn.Module):
    def forward(self, x_user, x_product, edge_label_index):
        return (x_user[edge_label_index[0]] * x_product[edge_label_index[1]]).sum(-1)


class Model(torch.nn.Module):
    def __init__(self, hidden_channels, metadata):
        super().__init__()
        self.gnn = GNN(hidden_channels)
        self.gnn = to_hetero(self.gnn, metadata=metadata)

        self.classifier = Classifier()

    def forward(self, data, embedding=False):
        x_dict = self.gnn(data.x_dict, data.edge_index_dict)

        if embedding:
            return x_dict
            
        pred = self.classifier(
            x_dict["user"],
            x_dict["product"],
            data["user", "buys", "product"].edge_label_index,
        )

        return pred