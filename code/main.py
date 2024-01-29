# число независимого доминирования и число совершенного геодоминирования
from sys import stdin
import networkx as nx
import matplotlib.pyplot as plt
import time
from itertools import combinations


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
    maximal_independent_sets = find_maximal_independent_sets(g)
    maximal_independent_sets.sort(key=len)
    for s in maximal_independent_sets:
        if nx.is_dominating_set(g, s):
            return len(s)


# 1 Найти кратчайшие пути между всеми вершинами
# 2 Выбираю две несвязные вершины в S, потом если что добавляю другие несвязные,
#   если такие есть
# 3 Каждая вершина из V = V\S должна принадлежать одному кратчайшему пути между вершинами в S

def find_perfect_geodominating_sets(g):
    nodes = set(g.nodes)
    # paths = dict(nx.all_pairs_shortest_path(g))
    for k in range(2, len(nodes)):
        # Всевозможные варианты множества вершин S
        for si in combinations(nodes, k):
            s = set(si)

            v = nodes - s
            # print('S =', si)
            # print('V\\S =', v)
            paths = []
            # Всевозможные кратчайшие пути между вершинами из S
            # TODO: может быть как-то эффективнее сохранять их, чтобы заново не считать?
            for pi in combinations(s, 2):
                for p in nx.all_shortest_paths(g, pi[0], pi[1]):
                    paths += p[1:-1]

            # print('Пути', paths)
            if len(paths) == 0:
                continue

            # TODO: Возможно достаточно проверить, совпадают ли пути с V\S (только отсортировать надо)
            # Ответ: не совсем, потому что если много вершин в S, то в путях могут быть вершины из S
            # Или не добавлять их, или проверять как реализовано
            flag = True
            for node in v:
                count = paths.count(node)
                # Если какая-то вершина из V\S встречается больше одного раза, значит
                # она геодоминируется несколькими парами вершин из S
                if count > 1 or count == 0:
                    # print('No', si)
                    flag = False
                    break

            if flag:
                # print('S', si)
                # print('V\\S', v)
                return len(si)
    # Если не получилось найти, значит в S должны быть все вершины
    # print('S', nodes)
    return len(nodes)


if __name__ == '__main__':
    # Вики - EEhW, word - FEhuO, HCOe`^w
    graphs6 = stdin.readlines()
    # graphs6 = ['FEhuO\n']
    t0 = time.time()

    for g6 in graphs6:
        g = nx.from_graph6_bytes(g6[0:-1].encode())
        # print('Граф', g6[0:-1].encode())
        # g = nx.from_graph6_bytes('FEhuO'.encode())
        # g = nx.Graph()
        # g.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1)])
        nx.draw(g, with_labels=True, font_weight='bold')
        # print('Число независимого доминирования', independent_domination_number(g))
        # print('Результат', find_perfect_geodominating_sets(g))
        # independent_domination_number(g)  # 7 - 26
        find_perfect_geodominating_sets(g)  # 7 - 30, 8 -


        # print(nx.maximal_independent_set(g))
        # plt.show()

    print(f'Время работы: {time.time() - t0} сек.')
