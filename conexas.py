import argparse
import io

from grafo import Grafo


def CFC(G):
    C, T, A_linha, F = DFS(G)
    A_t = list()
    w_t = dict()
    for u, v in G.E:
        A_t.append((v, u))
        w_t[(v, u)] = G.w[(u, v)]

    G_t = Grafo(G.V, A_t, w_t, rep=G._rep, eps=G._eps)

    # Chamar DFS alterado para que ele execute o o for em ordem decrescente de F
    C_t, T_t, A_linha_t, F_t = DFS(G_t, F_t=F)

    return A_linha_t

def DFS(G, F_t=None):
    # controla se o i-ésimo (-1) vértice já foi visitado
    C = G.qtdVertices() * [False, ]
    # tempo inicio
    T = G.qtdVertices() * [float('inf'), ] # como setar esses valores para infinito
    # tempo fim
    F = G.qtdVertices() * [float('inf'), ] # como setar esses valores para infinito
    # antecessor do i-ésimo (-1) vértice
    A = G.qtdVertices() * [None, ]
    # configurando o tempo de inicio

    tempo = 0

    V_ = list(range(1, G.n+1))

    if F_t is not None:
        V_ = [v for _, v in sorted(zip(F_t, V_), reverse=True)]

    for v in V_:
        if C[v-1] == False:
            # chama algotimo 17
            C, T, A, F, tempo = DFS_visit(G, v, C, T, A, F, tempo)

    return C, T, A, F

def DFS_visit(G, v, C, T, A, F, tempo):
    C[v-1] = True
    tempo = tempo + 1
    T[v-1] = tempo
    for u in G.vizinhos(v):
        if C[u-1] == False:
            A[u-1] = v # antecessor de u = v
            C, T, A, F, tempo = DFS_visit(G, u, C, T, A, F, tempo)
    tempo = tempo + 1
    F[v-1] = tempo
    return C, T, A, F, tempo


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
            "6 e\n"
            "*arcs\n"
            "1 2 1.5\n"
            "2 3 2\n"
            "3 1 1\n"
            "3 4 1\n"
            "4 5 1\n"
            "5 4 1\n"
            "4 6 1\n"
        )
        G = Grafo.ler(f, eps=float('inf'))
        f.close()
    else:
        with open(args.arquivo) as f:
            G = Grafo.ler(f)

    A = CFC(G)

    # cria conjuntos unitários dos vértices
    C = dict()
    for u in range(1, G.qtdVertices() + 1):
        if A[u-1] is None:
            C[u-1] = {u}

    for u in range(1, G.qtdVertices() + 1):
        # descobre a raiz da árvore
        p = A[u-1]
        r = p
        while p is not None:
            r = p
            p = A[r-1]
        
        if r is not None:
            C[r-1].add(u)

    # mostra os componentes
    C = list(C.values())
    for c in C:
        c = [str(c_i) for c_i in c]
        print(', '.join(c))
