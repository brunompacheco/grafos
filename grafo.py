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
    def __init__(self, V:list, E:List[set], w:PesoArestas, rep='listaAdj', eps=0):
        """ Grafo não-dirigido e ponderado.

        Attributes:
            V: Lista dos rótulos dos vértices, seguindo a ordem, mas indexada
            em i-1, ou seja, o rótulo do i-ésimo vértice é V[i-1].
            E: Lista das arestas, onde cada aresta é representada por um
            conjunto (set) dos vértices, e.g., `{i, j}`.
            w: Dicionário que associa as arestas a seus pesos. Deve ser uma
            instância de PesoArestas, uma extensão de um dict com sets como
            chaves, ou seja, um `Dict[set, float]`.
            rep: Representação do grafo a ser utilizada. Pode ser `listaAdj`
            ou `matrizAdj`.
            eps: No caso do uso de uma matriz de adjacências, define o valor a
            ser utilizado para representar a não adjacência.
        """
        # esconde os attributos de construção de forma que eles só sejam
        # acessados pelos métodos @property, simulando imutabilidade
        self._V = V
        self._E = E
        self._w = w

        self._rep = rep
        self._eps = eps

        n = len(V)
        if rep == 'listaAdj':
            # self._grafo = len(V) * [set(),]
            # feito assim para que sejam criados múltiplos sets, e não
            # múltiplas referências para o mesmo set
            self._grafo = [set() for _ in range(n)]

            for e in E:
                w_e = w[e]
                u, v = self.e2uv(e)
                self._grafo[u-1].add((v, w_e))
                self._grafo[v-1].add((u, w_e))
        elif rep == 'matrizAdj':
            self._grafo = [[eps for _ in range(n)] for _ in range(n)]

            print('Aviso: a matriz implementada não é otimizada (constroi-se a'
                  ' matriz completa)')

            for e in E:
                w_e = w[e]
                u, v = self.e2uv(e)
                self._grafo[u-1][v-1] = w_e
                self._grafo[v-1][u-1] = w_e
        
        self._n = n

    @property
    def V(self):
        return self._V

    @property
    def E(self):
        return self._E

    @property
    def w(self):
        return self._w

    @property
    def eps(self):
        return self._eps

    @property
    def rep(self):
        return self._rep

    @property
    def n(self):
        return self._n

    def qtdVertices(self):
        return self.n

    def qtdArestas(self):
        return len(self.E)

    def grau(self, v):
        return len(self.vizinhos(v))

    def rotulo(self, v):
        return self.V[v-1]

    def vizinhos(self, v, com_peso=False):
        """ `com_peso` := False requer uma varredura dos vizinhos no caso de
        self.rep == 'listaAdj'.
        """
        if self.rep == 'listaAdj':
            if com_peso:
                return self._grafo[v-1]
            else:
                return {u[0] for u in self._grafo[v-1]}
        elif self.rep == 'matrizAdj':
            vizinhos = set()
            for i in range(self.n):
                u = i + 1

                peso = self._grafo[v-1][u-1]
                if peso != self.eps:
                    if com_peso:
                        vizinhos.add((u, peso))
                    else:
                        vizinhos.add(u)

            return vizinhos

    def haAresta(self, e:set):
        return e in self.E

    def peso(self, e:set):
        u, v = self.e2uv(e)
        if self.rep == 'matrizAdj':
            return self._grafo[u-1][v-1]
        elif self.rep == 'listaAdj':
            for v_ in self._grafo[u-1]:
                if v_[0] == v:
                    return v_[1]

        return self.eps

    @staticmethod
    def e2uv(e):
        """ Como representamos uma aresta `e` por um set, precisamos acessar
        seus elementos por um iterável.
        """
        e_ = iter(e)
        u = next(e_)
        v = next(e_)

        return u, v

    @classmethod
    def ler(cls, arquivo, rep='listaAdj', eps=0):
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

        return cls(V, E, w, rep=rep, eps=eps)


if __name__ == '__main__':
    # TESTES
    for rep in ['listaAdj', 'matrizAdj']:
        f = io.StringIO(
            "*vertices 3\n"
            "1 a\n"
            "2 b\n"
            "3 c\n"
            "*edges\n"
            "1 2 1.5\n"
            "2 3 2\n"
        )
        G = Grafo.ler(f, rep=rep)
        f.close()

        assert G.qtdArestas() == 2
        assert G.qtdVertices() == 3

        assert G.grau(1) == 1
        assert G.grau(2) == 2
        assert G.grau(3) == 1

        assert G.rotulo(1) == 'a'
        assert G.rotulo(2) == 'b'
        assert G.rotulo(3) == 'c'

        assert G.vizinhos(1, com_peso=False) == {2}
        assert G.vizinhos(2, com_peso=False) == {3, 1}
        assert G.vizinhos(1, com_peso=False) == {2}

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