import unionfind.quickUnion
import unionfind.quickFind
import project.GraphGenerator as GraphGenerator
import graph.Graph_AdjacencyList
from graph.Graph import Edge


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


def edgeGenerator(G):  # funziona solo per grafi implementati con liste di adiacenza
    for adj_item in G.adj.items():
        curr = adj_item[1].getFirstRecord()
        while True:
            if not curr:  # if curr is None
                break
            yield Edge(adj_item[0], curr.elem, None)
            curr = curr.next


def hasCycleUFTest(G, uf):
    """
    Controlla se il grafo ha un ciclo sfruttando la struttura dati Union-Find. Per poter usare la stessa funzione
    in fase di testing, hasCycleUFTest prende in input un'istanza di tipo UnionFind vuota.
    :param G: Graph.
    :param uf: UnionFind.
    :return: bool.
    """
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


def printResults(G, func, *otherParameters):
    if func(G, *otherParameters):
        print("The graph has at least one cycle")
    else:
        print("The graph has no cycle")


if __name__ == "__main__":
    print("Acyclic:")
    acyclic = graph.Graph_AdjacencyList.GraphAdjacencyList()
    GraphGenerator.generateAcyclicGraph(acyclic, 10)
    printResults(acyclic, hasCycleUF)

    print("Cyclic:")
    cyclic = graph.Graph_AdjacencyList.GraphAdjacencyList()
    GraphGenerator.generateCyclicGraphNaive(cyclic, 10)
    printResults(cyclic, hasCycleUF)

    print("Random:")
    rand = graph.Graph_AdjacencyList.GraphAdjacencyList()
    print("Number of edges:", GraphGenerator.generateRandGraph(rand, 10))
    printResults(rand, hasCycleUF)

    print("Complete:")
    comp = graph.Graph_AdjacencyList.GraphAdjacencyList()
    GraphGenerator.generateCompleteGraph(comp, 10)
    printResults(comp, hasCycleUF)
