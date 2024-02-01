# число независимого доминирования и число совершенного геодоминирования
from sys import stdin
import networkx as nx
import matplotlib.pyplot as plt
import time
from itertools import combinations
import multiprocessing as mp


def find_maximal_independent_sets(g):
    # 1 Начальная установка
    k, s, q_minus, q_plus = 0, [], [[]], [list(g.nodes)]
    result = []

    def step2(k):
        xk = q_plus[k][0]
        s.append(xk)
        if k >= len(q_minus) - 1:
            q_minus.append([])
        else:
            q_minus[k + 1] = list(set(q_minus[k]) - set(g.adj[xk]))
        t_plus_k = q_plus[k].copy()
        t_plus_k.remove(xk)
        if k >= len(q_plus) - 1:
            q_plus.append(list(set(t_plus_k) - set(g.adj[xk])))
        else:
            q_plus[k + 1] = list(set(t_plus_k) - set(g.adj[xk]))
        k += 1
        # print(f'Шаг 2 \nk = {k}, xk = {xk} \nS = {s} \nQ+ = {q_plus} \nQ- = {q_minus}')
        return xk, k

    def step5(s, k):
        k -= 1
        xk = s[k]
        s.pop()
        q_plus[k].remove(xk)
        q_minus[k].append(xk)
        # print(f'Шаг 5 \nk = {k}, xk = {xk} \nS = {s} \nQ+ = {q_plus} \nQ- = {q_minus}')
        return k

    while len(q_plus[0]) != 0:
        if k != 0:
            # 3 Проверка
            if xk in q_minus and set(g.adj[xk]) & set(q_plus[k]) == set():
                k = step5(s, k)
            else:
                # 4
                if len(q_plus[k]) == 0:
                    if len(q_minus[k]) == 0:
                        # print('=' * 40)
                        # print(f'{s} к результату')
                        result.append(s.copy())
                        # print('=' * 40)
                        k = step5(s, k)
                    else:
                        k = step5(s, k)
                else:
                    xk, k = step2(k)
        else:
            xk, k = step2(k)
    return result


def independent_domination_number(g):
    g = nx.from_graph6_bytes(g[0:-1].encode())
    maximal_independent_sets = find_maximal_independent_sets(g)
    maximal_independent_sets.sort(key=len)
    for s in maximal_independent_sets:
        if nx.is_dominating_set(g, s):
            return len(s)


def find_perfect_geodominating_sets(g):
    g = nx.from_graph6_bytes(g[0:-1].encode())
    nodes = set(g.nodes)
    nodes_len = len(nodes)
    all_paths = [[None] * nodes_len for _ in range(nodes_len)]

    for k in range(2, len(nodes)):
        # Всевозможные варианты множества вершин S
        for si in combinations(nodes, k):
            s = set(si)
            v = nodes - s
            # print('S =', si)
            # print('V\\S =', v)

            paths = []
            # Всевозможные кратчайшие пути между вершинами из S
            for a, b in combinations(s, 2):
                if all_paths[a][b] is None:
                    all_paths[a][b] = list(nx.all_shortest_paths(g, a, b))
                for p in all_paths[a][b]:
                    paths += p[1:-1]

            # print('Пути', paths)
            if len(paths) == 0:
                continue

            flag = True
            for node in v:
                count = paths.count(node)
                # Если какая-то вершина из V\S встречается больше одного раза, значит
                # она геодоминируется несколькими парами вершин из S. Или вершина не геод-ся вовсе
                if count != 1:
                    # print('No', si)
                    flag = False
                    break

            if flag:
                # print('S', si)
                # print('V\\S', v)
                return len(si)
    # Если не получилось найти, значит в S должны быть все вершины
    # print('S', nodes)
    return nodes_len


if __name__ == '__main__':
    graphs6 = stdin.readlines()
    t0 = time.time()
    g = nx.from_graph6_bytes(graphs6[0][0:-1].encode())
    num_nodes = len(g.nodes)

    agents = 4
    chunksize = 4
    with mp.Pool(processes=agents) as pool:
        result = pool.map(find_perfect_geodominating_sets, graphs6, chunksize)
        result2 = pool.map(independent_domination_number, graphs6, chunksize)

    table = [[0] * num_nodes for _ in range(num_nodes)]
    for a, b in zip(result, result2):
        table[a - 1][b - 1] += 1

    for row in table:
        print(row)


    print(f'Время работы: {time.time() - t0} сек.')
