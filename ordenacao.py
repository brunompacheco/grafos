import argparse
import io
from grafo import Grafo


def DFS_ord_topologica(G: Grafo):
    # controla se o i-ésimo (-1) vértice já foi visitado
    C = G.qtdVertices() * [False, ]
    # tempo início
    T = G.qtdVertices() * [float("inf"), ]
    # tempo fim
    F = G.qtdVertices() * [float("inf"), ]
    
    tempo = 0

    # lista de vértices ordenados topologicamente
    O = []

    for v in range(1, G.qtdVertices() + 1):
        if C[v-1] == False:
            O = DFS_Visit(G, v, C, T, F, tempo, O)
    return O


def DFS_Visit(G: Grafo, v: int, C: list, T: list, F: list, tempo: int, O: list):
    tempo = tempo + 1

    C[v-1] = True
    T[v-1] = tempo

    for u in G.vizinhos(v):
        if C[u-1] == False:
            O = DFS_Visit(G, u, C, T, F, tempo, O) 
    tempo = tempo + 1
    F[v-1] = tempo

    O.insert(0,v)

    return O

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ordenação topológica.')
    parser.add_argument('arquivo', metavar='ARQUIVO', type=str)

    args = parser.parse_args()

    if args.arquivo == 'teste':
        f = io.StringIO(
            "*vertices 7\n"
            "1 a\n"
            "2 b\n"
            "3 c\n"
            "4 d\n"
            "5 e\n"
            "6 f\n"
            "7 g\n"
            "*arcs\n"
            "1 2 1\n"
            "1 7 1\n"
            "2 3 1\n"
            "2 4 1\n"
            "3 5 1\n"
            "5 6 1\n"
        )
        G = Grafo.ler(f, eps=float('inf'))
        f.close()
    else:
        with open(args.arquivo) as f:
            G = Grafo.ler(f)

    # mostra a ordenação pelos rótulos
    O = DFS_ord_topologica(G)

    rotulos = []
    for i in O:
        rotulos.append(G.rotulo(i))

    print(*rotulos, sep = ' -> ')
