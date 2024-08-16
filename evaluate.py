import os
import numpy as np
import pandas as pd


# Modularity
def modularity(index):
    cmu = nodes_per_cmu[index]
    lc = 0
    dc = 0
    for n in cmu:
        # lc += len(adj[n])
        if not adj.get(n):
            continue
        dc += len(adj[n])
        for m in adj[n]:
            # if m in cmu:
            if table[int(m)]:
                lc += 1
    lc /= 2
    # print(lc)
    return lc / E - dc * dc / (4 * E * E)

def vertex_density(index):
    cmu = nodes_per_cmu[index]
    ec = 0
    vc = len(cmu)
    for n in cmu:
        if not adj.get(n):
            continue
        # lc += len(adj[n])
        for m in adj[n]:
            # if m in cmu:
            if table[int(m)]:
                ec += 1
    ec /= 2

    return ec / vc

def edge_density(index):
    cmu = nodes_per_cmu[index]
    ec = 0
    vc = len(cmu)
    for n in cmu:
        if not adj.get(n):
            continue
        # lc += len(adj[n])
        for m in adj[n]:
            # if m in cmu:
            if table[int(m)]:
                ec += 1
    ec /= 2

    if vc - 1 <= 0:
        return -1
    return 2 * ec / (vc * (vc - 1))

def inverse_conductance(index):
    cmu = nodes_per_cmu[index]
    tc = 0
    lc = 0
    dc = 0
    for n in cmu:
        if not adj.get(n):
            continue
        tc += len(adj[n])
        dc += len(adj[n])
        for m in adj[n]:
            # if m in cmu:
            if table[int(m)]:
                lc += 1
    c_ = (tc - lc) / 2

    return 1 - c_ / dc

def size(index):
    return len(nodes_per_cmu[index])
        
# 计算 'modularity', 'vertex_density', 'edge_density', 'inverse_conductance', 'siz
def run_undirected(name):
    # with open('{}.query'.format(name), 'r') as fr:
    #     query_nodes = fr.read().strip().split('\n')
    # query_nodes = [t.strip() for t in query_nodes]
    #
    # community_list = []
    # with open('{}.gt'.format(name), 'r') as fr:
    #     for line in fr:
    #         community_list.append([t.strip() for t in line.strip().split(' ')])

    total_nodes = 0
    # 去重
    # temp = set()
    # with open('{}.gt'.format(name), 'r') as fr:
    #     for line in fr:
    #         temp.add(line)
    # with open('{}_duplicate.gt'.format(name), 'w') as fw:
    #     for item in temp:
    #         fw.write(item)

    nodes_per_cmu = []
    with open('{}_duplicate.gt'.format(name), 'r') as fr:
        for line in fr:
            line = set(line.strip().split(' '))
            for t in line:
                if int(t) > total_nodes:
                    total_nodes = int(t)
            nodes_per_cmu.append(line)
    total_nodes += 1

    # 创建邻接表
    adj = {}
    E = 0  # 创建邻接表时遍历图中总边数
    with open('{}.edges'.format(name), 'r') as fr:
        for line in fr:
            line = line.strip()
            if line == '':
                continue
            E += 1
            line = line.split(' ')
            if not adj.get(line[0]):
                adj[line[0]] = {line[1]}
            else:
                adj[line[0]].add(line[1])
    E /= 2  # 无向图总边长 / 2



    data_reserved = np.zeros((len(nodes_per_cmu) + 1, 5))
    index_labels = []
    for i in range(len(nodes_per_cmu)):
        table = np.zeros(total_nodes)
        for t in nodes_per_cmu[i]:
            # print(int(t))
            table[int(t)] = 1
        # print("{}:".format(name))

        index_labels.append('{} {}:'.format(name, i + 1))
        data_reserved[i, 0] = modularity(i)
        data_reserved[-1, 0] += data_reserved[i, 0]
        data_reserved[i, 1] = vertex_density(i)
        data_reserved[-1, 1] += data_reserved[i, 1]
        data_reserved[i, 2] = edge_density(i)
        data_reserved[-1, 2] += data_reserved[i, 2]
        data_reserved[i, 3] = inverse_conductance(i)
        data_reserved[-1, 3] += data_reserved[i, 3]
        data_reserved[i, 4] = size(i)
        data_reserved[-1, 4] += data_reserved[i, 4]

        # print('{} - class {}:'.format(name, i))
        # print('modularity:', end = ' ')
        # print(modularity(i))
        # print('vertex_density:', end = ' ')
        # print(vertex_density(i))
        # print('edge_density:', end = ' ')
        # print(edge_density(i))
        # print('inverse_conductance:', end = ' ')
        # print(inverse_conductance(i))
        # print('size:', end = ' ')
        # print(size(i))
        # print('------------------------')

    for i in range(data_reserved.shape[1]):
        data_reserved[-1, i] /= len(nodes_per_cmu)
    index_labels.append('{} mean'.format(name))

    return index_labels, data_reserved


if __name__ == '__main__':
    dataset_list = [
        "cornell", "texas", "wisconsin", "cora", "citeseer", "dblp", "physics", "photo", "cs"
    ]
    labels = [
        'modularity', 'vertex_density', 'edge_density', 'inverse_conductance', 'size'
    ]
    # "reddit"
    # idx, data = run_undirected('reddit')
    # df = pd.DataFrame(data, columns = labels, index = idx)
    # df.to_excel('res_reddit.xlsx')

    path = './data/'
    start = True
    for name in dataset_list:
        if start:
            idx, data = run_undirected(name)
            start = False
            continue
        # name = 'physics'
        t0, t1 = run_undirected(os.path.join(path, name))
        data = np.concatenate([data, t1], axis = 0)
        idx += t0

    df = pd.DataFrame(data, columns = labels, index = idx)
    # df.set_index('class', inplace = True)
    df.to_excel('res.xlsx')
