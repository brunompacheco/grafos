import argparse
import io

from copy import copy

from grafo import Grafo


def bfs_hopcroft_karp(G, X, Y, mate, D):
    Q = list()
    for x in X:
        if mate[x-1] == None:
            D[x-1] = 0
            Q.append(x)
        else:
            D[x-1] = float('inf')
    
    D[None] = float('inf')
    for x in Q:
        if x is not None:
            if D[x-1] < D[None]:
                for y in G.vizinhos(x):
                    mate_y = mate[y-1]
                    mate_y = mate_y - 1 if mate_y is not None else mate_y
                    if D[mate_y] == float('inf'):
                        D[mate_y] = D[x-1] + 1
                        Q.append(mate[y-1])
    
    bfs = D[None] != float('inf')
    return bfs, mate, D

def dfs_hopcroft_karp(G, x, mate, D):
    if x != None:
        for y in G.vizinhos(x):
            # mate[y-1] pode ser o índice do vértice (não 0-based) ou None
            mate_y = mate[y-1]
            mate_y = mate_y - 1 if mate_y is not None else mate_y
            if D[mate_y] == D[x-1] + 1:
                dfs, mate, D = dfs_hopcroft_karp(G, mate_y, mate, D)
                if dfs:
                    mate[y-1] = x
                    mate[x-1] = y
                    return True, mate, D
        D[x-1] = float('inf')
        return False, mate, D
    return True, mate, D

def hopcroft_karp(G, X, Y):
    D = G.qtdVertices() * [float('inf'), ]
    D = {k: v for k, v in enumerate(D)}  # convert to dict to support None

    mate = G.qtdVertices() * [None, ]

    m = 0

    bfs, mate, D = bfs_hopcroft_karp(G, X, Y, mate, D)
    while bfs:
        for x in X:
            if mate[x-1] == None:
                dfs, mate, D = dfs_hopcroft_karp(G, x, mate, D)
                if dfs:
                    m += 1

        bfs, mate, D = bfs_hopcroft_karp(G, X, Y, mate, D)

    return m, mate

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Emparelhamento máximo.')
    parser.add_argument('arquivo', metavar='ARQUIVO', type=str,
                        help="Grafo bipartido V=X `\\cup` Y. Cada vértice deve"
                        " ser nomeado 'X' ou 'Y' dependendo do conjunto do"
                        " qual participar.")

    args = parser.parse_args()

    if args.arquivo == 'teste':
        f = io.StringIO(
            "*vertices 7\n"
            "1 X\n"
            "2 X\n"
            "3 X\n"
            "4 Y\n"
            "5 Y\n"
            "6 Y\n"
            "7 Y\n"
            "*edges\n"
            "1 4 1\n"
            "2 5 1\n"
            "3 6 1\n"
            "3 7 1\n"
        )
        G = Grafo.ler(f, eps=float('inf'))  # capacidade, então eps = 0
        f.close()
    else:
        with open(args.arquivo) as f:
            G = Grafo.ler(f)

    X = [i+1 for i, l in enumerate(G.V) if l == 'X']
    Y = [i+1 for i, l in enumerate(G.V) if l == 'Y']

    # verifica se o grafo é bipartido
    assert len(set(X).intersection(set(Y))) == 0, "`X` e `Y` não são disjuntos"

    for e in G.E:
        u, v = G.e2uv(e)
        assert (u in X and v in Y) or (u in Y and v in X), "O grafo não é bipartido"

    m, mate = hopcroft_karp(G, X, Y)
    
    M = list()
    for u in range(1, G.n+1):
        v = mate[u-1]
        if v is not None:
            if {u,v} not in M:
                M.append({u,v})
    assert len(M) == m

    print(f"m = {m}")
    print(M)
