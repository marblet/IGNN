import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from torch_geometric.datasets import Planetoid
from torch_geometric.utils import add_self_loops

from allsumSVC import *
from allsumSLP import *
from learnProp import *
from improvedGCN import *

def draw_nx(graph, E, labels):
    graph = add_self_loops(graph)[0]
    edges = list(graph)
    weight = list(E.detach().numpy())
    edgelist = []
    weakedge = []
    strongedge = []
    for i, w in enumerate(weight):
        edgelist.append((int(edges[0][i]), int(edges[1][i]), float(w)))
        if w > 0.5:
            strongedge.append((int(edges[0][i]), int(edges[1][i])))
        else:
            weakedge.append((int(edges[0][i]), int(edges[1][i])))
    G = nx.Graph()
    G.add_weighted_edges_from(edgelist)
    y = list(labels)
    color = []
    for v in list(G):
        color.append(y[v])

    pos = nx.spring_layout(G, k=0.1)
    nx.draw_networkx_nodes(G, pos, node_color=color, node_size=50)
    # edge importance < 0.5
    nx.draw_networkx_edges(G, pos, edgelist=weakedge, edge_color='red', width=2.0)
    # edge importance > 0.5
    nx.draw_networkx_edges(G, pos, edgelist=strongedge, edge_color='black', width=0.5, alpha=0.1)
    plt.show()

if __name__ == "__main__":
    dataset = Planetoid(root='/tmp/Cora', name='Cora')
    # dataset = Planetoid(root='/tmp/Pubmed', name="Pubmed")
    # dataset = Planetoid(root='/tmp/Citeseer', name='Citeseer')
    data = dataset[0]
    features = data.x
    labels = data.y
    graph = data.edge_index
    train_mask = data.train_mask
    val_mask = data.val_mask
    test_mask = data.test_mask
    lam1 = 1e-3

    # svc_experiment(graph, features, labels, train_mask, test_mask, 3)
    # neural_experiment(graph, features, labels, train_mask, test_mask, 3)
    E = learnProp_experiment(graph, features, labels, train_mask, val_mask, test_mask, lam1)
    # improvedGCN(graph, features, labels, train_mask, val_mask, test_mask)

    draw_nx(graph, E, labels)
