import argparse
import io

from copy import copy

from grafo import Grafo


def caminho2arestas(p: tuple):
    p_ = list()

    for i in range(len(p) - 1):
        p_.append((p[i], p[i+1]))

    return p_

def get_residual(G: Grafo, f: dict):
    V_f = copy(G.V)

    E_f = copy(G.E)
    for e in G.E:
        u, v = G.e2uv(e)
        # adiciona arcos invertidos
        E_f.append((v, u))

    w_f = dict()
    for e in G.E:
        # arco do resíduo
        w_f[e] = G.w[e] - f[e]

        # arco invertido
        u, v = G.e2uv(e)
        w_f[(v, u)] = f[e]

    G_f = Grafo(V_f, E_f, w_f, eps=0)

    return G_f

def edmonds_karp(G_f: Grafo, s: int, t: int):
    # controla se o i-ésimo (-1) vértice já foi visitado
    C = G_f.qtdVertices() * [False, ]
    # antecessor do i-ésimo (-1) vértice
    A = G_f.qtdVertices() * [None, ]

    C[s-1] = True

    Q = [s]
    for u in Q: #  u=3
        for v in G_f.vizinhos(u): # v=4
            e = (u, v)
            if not C[v-1] and G_f.w[e] > 0:
                C[v-1] = True
                A[v-1] = u

                # criar caminho
                if v == t:
                    p = (t,)
                    w = t
                    while w != s:
                        w = A[w-1]
                        p = (w,) + p

                    return p

                Q.append(v)

    return None

def ford_fulkerson(G: Grafo, s: int, t: int):
    f = dict()
    for e in G.E:
        f[e] = 0

    G_f = get_residual(G, f)
    p = edmonds_karp(G_f, s, t)
    while p is not None:
        # capacidade do caminho aumentante
        c_f_p = min([G_f.w[e] for e in caminho2arestas(p)])

        # atualiza f a partir do caminho aumentante p
        for e in caminho2arestas(p):
            if e in G.E:
                f[e] += c_f_p
            else:
                u, v = G.e2uv(e)
                f[(v, u)] -= c_f_p

        G_f = get_residual(G, f)
        p = edmonds_karp(G_f, s, t)

    return f


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fluxo máximo.')
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
            "1 2 10\n"
            "1 3 5\n"
            "2 4 10\n"
            "2 5 5\n"
            "3 4 5\n"
            "4 6 10\n"
            "5 6 5\n"
        )
        G = Grafo.ler(f, eps=0)  # capacidade, então eps = 0
        f.close()
    else:
        with open(args.arquivo) as f:
            G = Grafo.ler(f)

    # assume-se que os vértices de origem e destino são o primeiro e o último
    # vértices declarados, resp.
    s = 1
    t = G.n

    # verifica se o grafo é uma rede de fluxo
    for e in G.E:
        u, v = G.e2uv(e)
        assert not G.haAresta((v, u)), "O grafo não é uma rede de fluxo."
        # nós não corrigimos o caso (u,v), (v,u) \in E

    f = ford_fulkerson(G, s, t)

    F = 0
    for v in G.vizinhos(s):
        e = (s, v)
        F += f[e]

    print(F)
