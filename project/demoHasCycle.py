from project.demoHasCycleUF import writeResults
import unionfind.quickUnion
import project.GraphGenerator as GraphGenerator
import graph.Graph_AdjacencyList
import random


@writeResults
def hasCycleDFS(G, rand=False):
    """
    Esegue una visita DFS nel grafo G a partire dal primo nodo, o da un nodo random, aseconda del parametro rand.
    Mantiene bool di marcatura per ogni nodo tramite indicizzazione diretta su una lista, verifica se ci sono archi
    all'indietro, ovvero da un nodo ad uno già visitato che non ne sia il padre. Se non ci sono archi all'indietro
    il grafo è aciclico.
    :param G: Graph.
    :param rand: bool.
    :return: bool.
    """
    if rand:
        rootId = random.choice(list(G.nodes.keys()))  # inizia la visita da un nodo random
    else:
        rootId = list(G.nodes.keys())[0]
    visited = [False for _ in G.nodes]  # inizializza la lista di marcatura
    return hasCycleDFSRecursive(G, rootId, visited, rootId)  # inizia la visita vera e propria


def hasCycleDFSRecursive(G, v, visited, fatherId):
    visited[v] = True  # marca il nodo v come visitato
    for adjNode in G.getAdj(v):
        if not visited[adjNode]:
            if hasCycleDFSRecursive(G, adjNode, visited, v):  # se la chiamata ricorsiva individua un ciclo
                return True  # ritorna True
        elif adjNode != fatherId:
            return True

    return False


class EdgesIterator:
    def __init__(self, G):
        self.n = -1
        self.edges = G.getEdges()
        self.lastIndex = len(self.edges) - 1

    def __iter__(self):
        return self

    def __next__(self):
        self.n += 1
        if self.n > self.lastIndex:
            raise StopIteration
        return self.edges[self.n]


@writeResults
def hasCycleUF(G):
    """
    Controlla se il grafo ha un ciclo sfruttando la struttura dati Union-Find.
    :param G: Graph.
    :return: bool.
    """
    uf = unionfind.quickUnion.QuickUnionBalanced()
    for n in G.nodes.keys():
        uf.makeSet(n)
    marked = set()
    for edge in EdgesIterator(G):
        if (edge.head, edge.tail) in marked:
            continue
        else:
            # aggiungi solo l'arco (edge.tail, edge.head) a marked, dato che (edge.head, edge.tail)
            # non verrà più generato dall'iterator
            marked.add((edge.tail, edge.head))
        if uf.find(uf.nodes[edge.head]) == uf.find(uf.nodes[edge.tail]):
            return True

        else:
            uf.union(uf.findRoot(uf.nodes[edge.head]), uf.findRoot(uf.nodes[edge.tail]))

    return False


def repeatedTest(func, typeOfGraph, maxN, steps, *otherParameters):
    # per semplicita' si assuma maxN % steps = 0
    assert typeOfGraph in range(4)
    file = open("{}.txt".format(func.__name__), "a")

    delta = int(maxN / steps)

    if typeOfGraph == 0:
        file.write("Acyclic:\n")
    elif typeOfGraph == 1:
        file.write("Cyclic:\n")
    elif typeOfGraph == 2:
        file.write("Random:\n")
    else:
        file.write("Complete:\n")

    file.close()

    temp = delta
    while temp <= maxN:
        G = graph.Graph_AdjacencyList.GraphAdjacencyList()
        if typeOfGraph == 0:
            GraphGenerator.generateAcyclicGraph(G, temp)
        elif typeOfGraph == 1:
            GraphGenerator.generateCyclicGraphNaive(G, temp)
        elif typeOfGraph == 2:
            GraphGenerator.generateRandGraph(G, temp)
        else:
            GraphGenerator.generateCompleteGraph(G, temp)

        func(G, *otherParameters)
        temp += delta

    print("Done!")


if __name__ == "__main__":
    for i in range(4):
        if i == 3:
            repeatedTest(hasCycleUF, i, 2000, 10)  # build a smaller graph if complete
        else:
            repeatedTest(hasCycleUF, i, 5000, 10)
    for i in range(4):
        if i == 1:
            repeatedTest(hasCycleDFS, i, 5000, 10, True)  # select a random rootId if graph is cyclic
        elif i == 3:
            repeatedTest(hasCycleDFS, i, 2000, 10)  # build a smaller graph if complete
        else:
            repeatedTest(hasCycleDFS, i, 5000, 10)
