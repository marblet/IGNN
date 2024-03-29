import numpy as np
import torch


def accuracy(pred, labels):
    _, indices = torch.max(pred, 1)
    correct = (indices == labels).sum().item()
    return correct / labels.size()[0]


def divide_dataset(dataset, num_train_per_class, num_val, num_test):
    num_class = dataset.num_classes
    data = dataset[0]
    labels = data.y
    n = data.num_nodes
    train_index = []
    for i in range(num_class):
        train_index.append(np.random.choice(np.where(labels == i)[0], size=num_train_per_class, replace=False))
    train_index = np.concatenate(train_index)
    remains = np.setdiff1d(np.arange(n), train_index)
    random_remains = np.random.permutation(remains)
    val_index = random_remains[:num_val]
    test_index = random_remains[num_val: num_val+num_test]
    train_mask = sample_mask(train_index, n)
    val_mask = sample_mask(val_index, n)
    test_mask = sample_mask(test_index, n)
    return train_mask, val_mask, test_mask


def sample_mask(index, num_nodes):
    mask = torch.zeros((num_nodes, ), dtype=torch.uint8)
    mask[index] = 1
    return mask


def eliminate_edges(edge_index, edge_importance, ratio=0.1, important=True):
    # if important == True, eliminate the important edges from edge_index
    n = edge_importance.size(0)
    num_elim = int(n * ratio)
    sorted_idx = torch.argsort(edge_importance[:, 0])
    if important:
        sorted_idx = sorted_idx[:n - num_elim]
    else:
        sorted_idx = sorted_idx[num_elim:]
    edge_index = edge_index[:, sorted_idx]
    return edge_index