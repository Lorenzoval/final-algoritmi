import unionfind.quickUnion
import unionfind.quickFind
import project.GraphGenerator as GraphGenerator
import graph.Graph_AdjacencyList
from functools import wraps
from time import time


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


def writeResults(func):
    @wraps(func)
    def wrapping_function(*args, **kwargs):
        start = time()
        value = func(*args, **kwargs)  # chiamata alla funzione da decorare
        elapsed = time() - start
        print(f'Function {func.__name__} took {elapsed} seconds')
        file = open("{}.txt".format(func.__name__), "a")
        file.write("{},{}\n".format(args[0].numEdges(), elapsed))
        file.close()
        print("Results written to file {}.txt".format(func.__name__))
        return value
    return wrapping_function


@writeResults
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


def repeatedTestUF(typeOfGraph, typeOfUF, maxN, steps):
    # per semplicita' si assuma maxN % steps = 0
    assert typeOfGraph in range(4)
    assert typeOfUF in range(6)
    file = open("hasCycleUFTest.txt", "a")

    delta = int(maxN / steps)

    if typeOfGraph == 0:
        file.write("Acyclic ")
    elif typeOfGraph == 1:
        file.write("Cyclic ")
    elif typeOfGraph == 2:
        file.write("Random ")
    else:
        file.write("Complete ")

    if typeOfUF == 0:
        file.write("QuickFind:\n")
    elif typeOfUF == 1:
        file.write("QuickFindBalanced:\n")
    elif typeOfUF == 2:
        file.write("QuickUnion:\n")
    elif typeOfUF == 3:
        file.write("QuickUnionBalanced:\n")
    elif typeOfUF == 4:
        file.write("QuickUnionBalancedPathCompression:\n")
    else:
        file.write("QuickUnionBalancedPathSplitting:\n")

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

        if typeOfUF == 0:
            uf = unionfind.quickFind.QuickFind()
        elif typeOfUF == 1:
            uf = unionfind.quickFind.QuickFindBalanced()
        elif typeOfUF == 2:
            uf = unionfind.quickUnion.QuickUnion()
        elif typeOfUF == 3:
            uf = unionfind.quickUnion.QuickUnionBalanced()
        elif typeOfUF == 4:
            uf = unionfind.quickUnion.QuickUnionBalancedPathCompression()
        else:
            uf = unionfind.quickUnion.QuickUnionBalancedPathSplitting()

        hasCycleUFTest(G, uf)
        temp += delta

    print("Done!")


if __name__ == "__main__":
    # test the various permutations
    for i in range(4):
        for j in range(6):
            if i == 3:
                repeatedTestUF(i, j, 2000, 10)  # the algorithm takes a lot of time on complete graphs
            else:
                repeatedTestUF(i, j, 5000, 10)
