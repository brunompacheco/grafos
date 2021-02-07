import argparse

from grafo import Grafo

def buscaLargura(G: Grafo, s):
    # controla se o i-ésimo (-1) vértice já foi visitado
    C = G.qtdVertices() * [False, ]
    # nível do i-ésimo (-1) vértice
    D = G.qtdVertices() * [-1, ]
    # antecessor do i-ésimo (-1) vértice
    A = G.qtdVertices() * [None, ]

    C[s-1] = True
    D[s-1] = 0

    Q = [s]
    for u in Q:
        for v, _ in G.vizinhos(u, com_peso=True):
            if not C[v-1]:
                C[v-1] = True
                D[v-1] = D[u-1] + 1
                A[v-1] = u

                Q.append(v)

    return D, A


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Busca em largura.')
    parser.add_argument('arquivo', metavar='ARQUIVO', type=str)
    parser.add_argument('s', metavar='S', type=int)

    args = parser.parse_args()

    with open(args.arquivo) as f:
        G = Grafo.ler(f)

    D, A = buscaLargura(G, args.s)

    niveis = dict()
    for u in range(1, G.qtdVertices() + 1):
        i = D[u-1]
        if i not in niveis.keys():
            niveis[i] = [str(u)]
        else:
            niveis[i].append(str(u))

    for i in sorted(niveis.keys()):
        vertices = ', '.join(niveis[i])
        print(str(i) + ": " + vertices)
