import io

from typing import List, Set, Dict


class PesoArestas(dict):
    def __init__(self, *args):
        super().__init__(args)

    def __getitem__(self, key):
        if isinstance(key, set):
            return super().__getitem__(tuple(key))
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, val):
        if isinstance(key, set):
            super().__setitem__(tuple(key), val)
        else:
            super().__setitem__(key, val)

class Grafo():
    def __init__(self, V:list, E:List[set], w:PesoArestas):
        """ Grafo não-dirigido e ponderado.

        Attributes:
            V: Lista dos rótulos dos vértices, seguindo a ordem, mas indexada
            em i-1.
            E: Lista das arestas, onde cada aresta é representada por um
            conjunto (set) dos vértices, e.g., `{i, j}`.
            w: Dicionário que associa as arestas a seus pesos. Deve ser uma
            instância de PesoArestas, uma extensão de um dict com sets como
            chaves, ou seja, um `Dict[set, float]`.
        """
        self.V = V
        self.E = E
        self.w = w

    def qtdVertices(self):
        return len(self.V)

    def qtdArestas(self):
        return len(self.E)

    def grau(self, v):
        arestas_com_v = [v in e for e in self.E]

        return sum(arestas_com_v)

    def rotulo(self, v):
        return self.V[v-1]  # TODO: verificar se essa é a interpretação de `v`

    def vizinhos(self, v):
        vizinhos_v = [set(e) for e in self.E if v in e]
        vizinhos_v = set().union(*vizinhos_v)
        vizinhos_v.remove(v)

        return vizinhos_v

    def haAresta(self, e:set):
        return e in self.E

    def peso(self, e:set):
        if self.haAresta(e):
            return self.w[e]
        else:
            return float('inf')

    @classmethod
    def ler(cls, arquivo):
        linhas = arquivo.readlines()
        linhas = [l.replace('\n', '').replace('\r', '') for l in linhas]

        # primeira linha no formato `*vertices n`
        n_vertices = int(linhas[0].split(' ')[-1])

        # vertices representados como `i rotulo_de_i`
        vertices = linhas[1:n_vertices+1]
        vertices = [v.split(' ')[-1] for v in vertices]
        V = vertices

        arestas = linhas[n_vertices+2:]  # n+2 por causa do label `*edges`
        arestas = [e.split(' ') for e in arestas]
        E = list()
        w = PesoArestas()
        for a, b, valor in arestas:
            e = {int(a), int(b)}
            E.append(e)
            w[e] = float(valor)

        return cls(V, E, w)


if __name__ == '__main__':
    # TESTES
    f = io.StringIO(
        "*vertices 3\n"
        "1 a\n"
        "2 b\n"
        "3 c\n"
        "*edges\n"
        "1 2 1.5\n"
        "2 3 2\n"
    )
    G = Grafo.ler(f)

    assert G.qtdArestas() == 2
    assert G.qtdVertices() == 3

    assert G.grau(1) == 1
    assert G.grau(2) == 2
    assert G.grau(3) == 1

    assert G.rotulo(1) == 'a'
    assert G.rotulo(2) == 'b'
    assert G.rotulo(3) == 'c'

    assert G.vizinhos(1) == {2}
    assert G.vizinhos(2) == {3, 1}
    assert G.vizinhos(1) == {2}

    assert G.haAresta({1, 2}) == True
    assert G.haAresta({2, 1}) == True
    assert G.haAresta({2, 3}) == True
    assert G.haAresta({3, 2}) == True
    assert G.haAresta({3, 1}) == False
    assert G.haAresta({1, 3}) == False

    assert G.peso({1, 2}) == 1.5
    assert G.peso({2, 1}) == 1.5
    assert G.peso({2, 3}) == 2.0

    print('Success')