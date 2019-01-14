from project.demoHasCycleUF import writeResults
import project.GraphGenerator as GraphGenerator
import graph.Graph_AdjacencyList
import graph.Graph_IncidenceList
import graph.Graph_AdjacencyMatrix


@writeResults
def hasCycleDFSTest(G):
    """
    Esegue una visita DFS nel grafo G a partire dal primo nodo. Mantiene bool di marcatura per ogni nodo
    tramite indicizzazione diretta su una lista, verifica se ci sono archi all'indietro, ovvero da un nodo
    ad uno già visitato che non ne sia il padre. Se non ci sono archi all'indietro il grafo è aciclico.
    :param G: Graph.
    :return: bool.
    """
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


def repeatedTest(graphImpl, maxN, steps):
    # per semplicita' si assuma maxN % steps = 0
    assert graphImpl in range(3)
    file = open("hasCycleDFSTest.txt", "a")

    delta = int(maxN / steps)

    if graphImpl == 0:
        file.write("AdjacencyList:\n")
    elif graphImpl == 1:
        file.write("IncidenceList:\n")
    else:
        file.write("AdjacencyMatrix:\n")

    file.close()

    temp = delta
    while temp <= maxN:
        if graphImpl == 0:
            G = graph.Graph_AdjacencyList.GraphAdjacencyList()
        elif graphImpl == 1:
            G = graph.Graph_IncidenceList.GraphIncidenceList()
        else:
            G = graph.Graph_AdjacencyMatrix.GraphAdjacencyMatrix()
        GraphGenerator.generateRandGraph(G, temp)

        hasCycleDFSTest(G)
        temp += delta

    print("Done!")


if __name__ == "__main__":
    for i in range(3):
        repeatedTest(i, 5000, 10)
