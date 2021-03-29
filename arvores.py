import argparse
import io

from copy import copy
from heapq import heapify, heappop, heappush
from random import randint

from grafo import Grafo


def prim(G: Grafo):
    # vértice arbitrário de G
    r = randint(1, G.n)

    # antecessor do i-ésimo (-1) vértice
    A = G.qtdVertices() * [None, ]
    K = G.qtdVertices() * [float('inf'), ]
    K[r-1] = 0

    Q = list(zip(K, range(1, G.n + 1)))
    heapify(Q)
    V_q = set(range(1, G.n + 1))  # para manter controle dos vértices visitados
    while len(V_q) > 0:
        k_u, u = heappop(Q)
        try:
            V_q.remove(u)
        except KeyError:
            # if `u` was already visited
            continue

        for v in G.vizinhos(u):
            w_uv = G.peso({u, v})
            if v in V_q and w_uv < K[v-1]:
                A[v-1] = u
                K[v-1] = w_uv
                heappush(Q, (w_uv, v))

    return A

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Componentes Fortemente Conexas.')
    parser.add_argument('arquivo', metavar='ARQUIVO', type=str)

    args = parser.parse_args()

    if args.arquivo == 'teste':
        f = io.StringIO(
            "*vertices 6\n"
            "1 a\n"
            "2 b\n"
            "3 c\n"
            "4 d\n"
            "5 e\n"
            "6 f\n"
            "*edges\n"
            "1 2 1\n"
            "1 4 4\n"
            "1 5 3\n"
            "2 4 4\n"
            "2 5 2\n"
            "4 5 4\n"
            "3 5 4\n"
            "3 6 5\n"
            "5 6 7\n"
        )
        G = Grafo.ler(f, eps=float('inf'))
        f.close()
    else:
        with open(args.arquivo) as f:
            G = Grafo.ler(f)

    A = prim(G)

    E_arv = list()
    soma_E_arv = 0
    for v in range(1, G.n + 1):
        u = A[v-1]
        if u is not None:
            e = {u, v}
            soma_E_arv += G.peso(e)
            E_arv.append(tuple(e))

    E_arv = [f"{u}-{v}" for u, v in E_arv]

    print(soma_E_arv)
    print(', '.join(E_arv))
