import project.GraphGenerator as GraphGenerator
import graph.Graph_AdjacencyList
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
        elif visited[adjNode] and adjNode != fatherId:
            return True

    return False


def printResults(G):
    if hasCycleDFS(G):
        print("The graph has at least one cycle")
    else:
        print("The graph has no cycle")


if __name__ == "__main__":
    print("Acyclic:")
    acyclic = graph.Graph_AdjacencyList.GraphAdjacencyList()
    GraphGenerator.generateAcyclicGraph(acyclic, 10)
    printResults(acyclic)

    print("Cyclic:")
    cyclic = graph.Graph_AdjacencyList.GraphAdjacencyList()
    GraphGenerator.generateCyclicGraphNaive(cyclic, 10)
    printResults(cyclic)

    print("Random:")
    rand = graph.Graph_AdjacencyList.GraphAdjacencyList()
    print("Number of edges:", GraphGenerator.generateRandGraph(rand, 10))
    printResults(rand)

    print("Complete:")
    comp = graph.Graph_AdjacencyList.GraphAdjacencyList()
    GraphGenerator.generateCompleteGraph(comp, 10)
    printResults(comp)
