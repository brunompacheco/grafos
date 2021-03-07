import argparse
import io

from copy import copy
from random import randint

from grafo import Grafo, PesoArestas


def subcicloEuleriano(G: Grafo, v, C: PesoArestas):
    ciclo = [v]
    t = v
    while True:
        for u in G.vizinhos(v, com_peso=False):
            if C[{v, u}] == False:
                break
        else:
            return False

        C[{v, u}] = True

        v = u

        ciclo.append(v)

        if v == t:
            break
    
    vertices_restantes = list()
    for u in set(ciclo):
        vizinhos_restantes_u = [w for w in G.vizinhos(u, com_peso=False) if C[{u, w}] == False]
        if len(vizinhos_restantes_u) > 0:
            vertices_restantes.append(u)

    for x in vertices_restantes:
        ciclo_ = subcicloEuleriano(G, x, C)

        if ciclo_ == False:
            return False
        
        x_i = ciclo.index(x)

        ciclo = ciclo[:x_i] + ciclo_ + ciclo[x_i+1:]

    return ciclo


def cicloEuleriano(G: Grafo):
    """ Implementação do algoritmo de Hierholzer.
    """
    C = copy(G.w)
    for e in C.keys():
        C[e] = False

    # seleciona um vértice aleatoriamente
    v = randint(1, G.qtdVertices())

    ciclo = subcicloEuleriano(G, v, C)

    if not all(C.values()):
        return False
    else:
        return ciclo

D_validos = list()
for v in G.V:
    if C[v] == False:
        D_validos.append(D[v])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ciclo Euleriano.')
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
        G = Grafo.ler(f)
        f.close()
    else:
        with open(args.arquivo) as f:
            G = Grafo.ler(f)

    ciclo = cicloEuleriano(G)

    if ciclo != False:
        print(1)
        print(ciclo)
    else:
        print(0)
