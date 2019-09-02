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

def draw_nx(graph, labels):
    G = nx.from_edgelist(np.array(graph).T)
    y = list(labels)
    color = []
    for v in list(G):
        color.append(y[v])
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, k=1, node_color=color)
    plt.show()

def draw_tsne(graph, E, labels):
    graph = add_self_loops(graph)[0]
    edges = list(graph)
    weight = list(E.detach().numpy())
    edgelist = []
    for i, w in enumerate(weight):
        edgelist.append((int(edges[0][i]), int(edges[1][i]), float(w)))
    G = nx.Graph()
    G.add_weighted_edges_from(edgelist)

    G = nx.from_edgelist(np.array(graph).T)
    A = nx.to_numpy_matrix(G)
    y = list(labels)
    color = []
    for v in list(G):
        color.append(y[v])
    X_reduced = TSNE(n_components=2, random_state=0, n_iter=2000).fit_transform(A, y=color)
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=color)
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
    lam1 = 0

    # svc_experiment(graph, features, labels, train_mask, test_mask, 3)
    # neural_experiment(graph, features, labels, train_mask, test_mask, 3)
    E = learnProp_experiment(graph, features, labels, train_mask, val_mask, test_mask, lam1)
    # improvedGCN(graph, features, labels, train_mask, val_mask, test_mask)

    draw_nx(graph, labels)
    # draw_tsne(graph, E, labels)

