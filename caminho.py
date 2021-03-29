import argparse
import io

from grafo import Grafo


def floydWarshall(G: Grafo):
    D = (G.n+1) * [None, ]
    for k in range(G.n + 1):
        D[k] = [[G.eps for _ in G.V] for _ in G.V]

        if k == 0:
            for v in range(1, G.n+1):
                D[k][v-1][v-1] = 0

            for e in G.E:
                u, v = G.e2uv(e)
                D[k][u-1][v-1] = G.peso(e)
                D[k][v-1][u-1] = G.peso(e)
        else:
            for u in range(1, G.n+1):
                for v in range(1, G.n+1):
                    D[k][u-1][v-1] = min(D[k-1][u-1][v-1], D[k-1][u-1][k-1] + D[k-1][k-1][v-1])

    return D[-1]


def dijkstra(G: Grafo, s):
    # varre a lista de pesos e verifica se existe algum peso negativo
    assert all([w_e >=0 for w_e in G.w.values()])

    # controla se o i-ésimo (-1) vértice já foi visitado
    C = G.qtdVertices() * [False, ]
    # nível do i-ésimo (-1) vértice
    D = G.qtdVertices() * [G.eps, ]
    # antecessor do i-ésimo (-1) vértice
    A = G.qtdVertices() * [None, ]
    # distância do nodo inicial s = 0
    D[s-1] = 0

    while not all(C):
        # seleciona o vértice de menor custo 
        D_validos = list()
        v_validos = list()
        for v in range(1, G.qtdVertices() + 1):
            if C[v-1] == False:
                D_validos.append(D[v-1])
                v_validos.append(v)
        D_min = min(D_validos)
        u_i = D_validos.index(D_min)
        u = v_validos[u_i]
        C[u-1] = True

        for v in G.vizinhos(u):
            if (D[v-1] > D[u-1] + G.peso({u,v})):
                D[v-1] = D[u-1] + G.peso({u,v})
                A[v-1] = u
    return D, A # Retorna lista níveis ("distâncias") e antecessores


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Caminho mínimo.')
    parser.add_argument('arquivo', metavar='ARQUIVO', type=str)
    parser.add_argument('alg', metavar='ALGORITMO', type=str)
    parser.add_argument('--s', dest='source', type=int, default=1)

    args = parser.parse_args()

    if args.arquivo == 'teste':
        f = io.StringIO(
            "*vertices 9\n"
            "1 a\n"
            "2 b\n"
            "3 c\n"
            "4 d\n"
            "5 e\n"
            "6 f\n"
            "7 g\n"
            "8 g\n"
            "9 g\n"
            "*edges\n"
            "1 2 1\n"
            "2 3 1\n"
            "3 4 1\n"
            "4 5 1\n"
            "5 6 1\n"
            "6 3 1\n"
            "3 7 1\n"
            "7 1 1\n"
            "3 8 1\n"
            "8 9 1\n"
            "9 3 1\n"
        )
        G = Grafo.ler(f, eps=float('inf'))
        f.close()
    else:
        with open(args.arquivo) as f:
            G = Grafo.ler(f)

    if args.alg == 'floyd-warshall':
        D = floydWarshall(G)

        for i in range(1, G.n + 1):
            D_i = ', '.join([f"{D_ij:.1f}" for D_ij in D[i-1]])
            print(f"{i}: {D_i}")
    elif args.alg == 'dijkstra':
        D, A = dijkstra(G, args.source)
        for v in range(1, G.qtdVertices() + 1):
            caminho = []
            a = v # a = antecessor
            while a != None:
                caminho.append(str(a))
                a = A[a-1]
            caminho = caminho[::-1] # inverte a ordem do caminho percorrido

            print(str(v), ":", ','.join(caminho), ";","d =", str(D[v-1]))
    else:
        print(args.alg + ' not implemented')
