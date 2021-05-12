import argparse
import io

from itertools import product

import numpy as np

from networkx import Graph
from networkx.algorithms.mis import maximal_independent_set

from grafo import Grafo


def maximal_independent_subsets(G: Grafo, S: list):
    nxG = Graph()
    nxG.add_nodes_from(S)
    nxG.add_edges_from([tuple(e) for e in G.E if e.issubset(S)])

    miss = list()
    for i in range(5):
        mis = maximal_independent_set(nxG)
        if set(mis) not in miss:
            miss.append(set(mis))

    return [list(mis) for mis in miss]

def id2s(id):
    b = [str(int(x)) for x in id]
    b = '0b' + ''.join(b)
    return int(b, 2)

def lawler(G: Grafo):
    X = [None,] * (2**G.n)
    X[0] = 0

    S_idx = product(*[[False, True],]*G.n)
    S_idx = list(S_idx)[1:]

    V_idx = np.arange(G.n, 0, -1)

    for S_id in S_idx:
        S = V_idx[list(S_id)]

        s = id2s(S_id)

        X[s] = float('inf')

        if len(S) > 0:
            I_G_ = maximal_independent_subsets(G, S)
        else:
            I_G_ = list()

        for I in I_G_:
            S_diff_I = [v for v in S if v not in I]
            i = id2s(np.isin(V_idx, S_diff_I))
            if X[i] + 1 < X[s]:
                X[s] = X[i] + 1

    return X[-1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Coloração.')
    parser.add_argument('arquivo', metavar='ARQUIVO', type=str,
                        help="Grafo não dirigido e não ponderado.")

    args = parser.parse_args()

    if args.arquivo == 'teste':
        f = io.StringIO(
            "*vertices 4\n"
            "1 a\n"
            "2 b\n"
            "3 c\n"
            "4 c\n"
            "*edges\n"
            "1 2 1\n"
            "2 3 1\n"
            "2 4 1\n"
            "3 4 1\n"
            "4 1 1\n"
        )
        G = Grafo.ler(f, eps=float('inf'))  # capacidade, então eps = 0
        f.close()
    else:
        with open(args.arquivo) as f:
            G = Grafo.ler(f)

    print(lawler(G))
