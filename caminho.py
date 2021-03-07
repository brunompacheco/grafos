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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Caminho mínimo.')
    parser.add_argument('arquivo', metavar='ARQUIVO', type=str)

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

    D = floydWarshall(G)

    for i in range(1, G.n + 1):
        D_i = ', '.join([f"{D_ij:.1f}" for D_ij in D[i-1]])
        print(f"{i}: {D_i}")
