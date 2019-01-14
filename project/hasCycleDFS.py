import project.GraphGenerator as GraphGenerator
import graph.Graph_AdjacencyList
from datastruct.Stack import PilaArrayList as Stack
from time import time
# import random


def hasCycleDFS(G):
    """
    Esegue una visita DFS nel grafo G a partire dal primo nodo. Mantiene bool di marcatura per ogni nodo
    tramite indicizzazione diretta su una lista, verifica se ci sono archi all'indietro, ovvero da un nodo
    ad uno già visitato che non ne sia il padre. Se non ci sono archi all'indietro il grafo è aciclico.
    :param G: Graph.
    :return: bool.
    """
    # rootId = random.choice(list(G.nodes.keys()))  # inizia la visita da un nodo random
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


def hasCycleDFSIter(G):
    """
    Esegue una visita DFS nel grafo G a partire dal primo nodo. Se un nodo non ancora visitato si trova già
    nello stack, allora ai passi successivi si genererà un arco all'indietro, ovvero un arco da un nodo ad uno già
    visitato. È importante notare che per ogni nodo non viene preso in considerazione l'arco diretto verso il padre,
    poiché quest'ultimo è già marcato come visitato.
    :param G: Graph.
    :return: bool.
    """
    # rootId = random.choice(list(G.nodes.keys()))  # inizia la visita da un nodo random
    rootId = list(G.nodes.keys())[0]

    # DFS nodes initialization
    dfsNodes = set()

    # queue initialization
    s = Stack()
    s.push(rootId)

    explored = {rootId}  # nodes already explored

    while not s.isEmpty():  # while there are nodes to explore ...
        node = s.pop()  # get the node from the stack
        explored.add(node)  # mark the node as explored
        # add all adjacent unexplored nodes to the stack
        for adjNode in G.getAdj(node):
            if adjNode not in explored:
                s.push(adjNode)
        if node in dfsNodes:
            return True
        dfsNodes.add(node)

    return False


def printResults(G, func):
    if func(G):
        print("The graph has at least one cycle")
    else:
        print("The graph has no cycle")


if __name__ == "__main__":
    print("Acyclic:")
    acyclic = graph.Graph_AdjacencyList.GraphAdjacencyList()
    GraphGenerator.generateAcyclicGraph(acyclic, 10)
    printResults(acyclic, hasCycleDFS)

    print("Cyclic:")
    cyclic = graph.Graph_AdjacencyList.GraphAdjacencyList()
    GraphGenerator.generateCyclicGraphNaive(cyclic, 10)
    printResults(cyclic, hasCycleDFS)

    print("Random:")
    rand = graph.Graph_AdjacencyList.GraphAdjacencyList()
    print("Number of edges:", GraphGenerator.generateRandGraph(rand, 10))
    printResults(rand, hasCycleDFS)

    print("Complete:")
    comp = graph.Graph_AdjacencyList.GraphAdjacencyList()
    GraphGenerator.generateCompleteGraph(comp, 10)
    printResults(comp, hasCycleDFS)

    # small test
    comp2 = graph.Graph_AdjacencyList.GraphAdjacencyList()
    GraphGenerator.generateCompleteGraph(comp2, 500)
    start = time()
    hasCycleDFS(comp2)
    print("Recursive function took {} seconds".format(time() - start))
    start = time()
    hasCycleDFSIter(comp2)
    print("Iterative function took {} seconds".format(time() - start))
