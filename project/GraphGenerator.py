import graph.Graph_AdjacencyList
import graph.Graph_AdjacencyMatrix
import graph.Graph_IncidenceList
import numpy as np
import random


def generateAcyclicGraph(G, n, weighted=False):
    """
    generateAcyclicGraph, dato in input un grafo vuoto (non dipendendo quindi dall'implementazione dello stesso)
    lo modifica in loco rendendolo un grafo con n vertici non orienetato, connesso ed aciclico.
    Il parametro weighted indica se il grafo va generato pesato o non pesato. Ritorna il numero di archi.
    :param G: empty Graph.
    :param n: int.
    :param weighted: bool.
    :return: int.
    """
    edges = 0
    # check if the graph is weighted
    if not weighted:
        weight = None

    nodes = []
    # add nodes to G
    for i in range(n):
        nodes.append(G.addNode(i))
    # add edges to G
    linkedNodes = [nodes[0]]
    for j in nodes[1:]:
        dst = random.choice(linkedNodes)
        if weighted:
            weight = j.id + dst.id
        G.insertEdge(j.id, dst.id, weight)
        G.insertEdge(dst.id, j.id, weight)
        edges += 1
        linkedNodes.append(j)

    return edges


def generateCyclicGraphNaive(G, n, weighted=False):
    """
    generateCyclicGraphNaive, dato in input un grafo vuoto (non dipendendo quindi dall'implementazione dello stesso)
    lo modifica in loco rendendolo un grafo con n vertici non orienetato, connesso e con un ciclo.
    Il parametro weighted indica se il grafo va generato pesato o non pesato. Ritorna il numero di archi.
    :param G: empty Graph.
    :param n: int.
    :param weighted: bool.
    :return: int.
    """
    edges = 0
    # check if the graph is weighted
    if not weighted:
        weight = None

    nodes = []
    # add nodes to G
    for i in range(n):
        nodes.append(G.addNode(i))
    # build a cycle with the first 3 vertices
    linkedNodes = [nodes[0], nodes[1], nodes[2]]
    if weighted:
        weight = linkedNodes[0].id + linkedNodes[1].id
    G.insertEdge(linkedNodes[0].id, linkedNodes[1].id, weight)
    G.insertEdge(linkedNodes[1].id, linkedNodes[0].id, weight)
    edges += 1
    if weighted:
        weight = linkedNodes[1].id + linkedNodes[2].id
    G.insertEdge(linkedNodes[1].id, linkedNodes[2].id, weight)
    G.insertEdge(linkedNodes[2].id, linkedNodes[1].id, weight)
    edges += 1
    if weighted:
        weight = linkedNodes[0].id + linkedNodes[2].id
    G.insertEdge(linkedNodes[0].id, linkedNodes[2].id, weight)
    G.insertEdge(linkedNodes[2].id, linkedNodes[0].id, weight)
    edges += 1
    # add edges to G
    for j in nodes[3:]:
        dst = random.choice(linkedNodes)
        if weighted:
            weight = j.id + dst.id
        G.insertEdge(j.id, dst.id, weight)
        G.insertEdge(dst.id, j.id, weight)
        edges += 1
        linkedNodes.append(j)

    return edges
        
        
def generateRandGraph(G, n, weighted=False):
    """
    Dato in input un grafo G vuoto (non dipendendo quindi dall'implementazione dello stesso), lo modifica in loco
    generando un grafo con n vertici, connesso,non orientato, che può essere ciclico o aciclico.
    Il parametro weighted indica se il grafo va generato pesato o non pesato. Ritorna il numero di archi.
    :param G: empty Graph.
    :param n: int.
    :param weighted: bool.
    :return: int.
    """
    edges = 0
    # check if the graph is weighted
    if not weighted:
        weight = None

    nodes = []
    # add nodes to G
    for i in range(n):
        nodes.append(G.addNode(i))
    # add edges to G
    linkedNodes = [nodes[0]]

    for j in nodes[1:]:
        tempLen = len(linkedNodes)
        # generate a random number of edges for each node
        numEdges = max(1, np.random.binomial(tempLen, 1 / tempLen))
        alreadyLinked = []

        for _ in range(numEdges):
            dst = random.choice(linkedNodes)
            # if destination node is already linked to j, generate a new one
            while dst in alreadyLinked:
                dst = random.choice(linkedNodes)
            # add dst to the nodes already linked to j
            alreadyLinked.append(dst)

            # add edges to the graph
            if weighted:
                weight = j.id + dst.id
            G.insertEdge(j.id, dst.id, weight)
            G.insertEdge(dst.id, j.id, weight)
            # increase the counter of edges
            edges += 1
        linkedNodes.append(j)

    return edges


def generateCompleteGraph(G, n, weighted=False):
    """
    Dato in input un grafo G vuoto (non dipendendo quindi dall'implementazione dello stesso), lo modifica in loco
    generando un grafo con n vertici, non orientato, in cui ogni nodo è connesso con ogni altro nodo del grafo.
    Il parametro weighted indica se il grafo va generato pesato o non pesato. Ritorna il numero di archi.
    :param G: empty Graph.
    :param n: int.
    :param weighted: bool.
    :return: int.
    """
    edges = 0
    # check if the graph is weighted
    if not weighted:
        weight = None

    nodes = []
    # add nodes to G
    for i in range(n):
        nodes.append(G.addNode(i))
    # add edges to G
    linkedNodes = [nodes[0]]

    for j in nodes[1:]:
        tempLen = len(linkedNodes)

        for n in range(tempLen):
            # add edges from j to all the already linked nodes
            if weighted:
                weight = j.id + linkedNodes[n].id
            G.insertEdge(j.id, linkedNodes[n].id, weight)
            G.insertEdge(linkedNodes[n].id, j.id, weight)
            edges += 1
        linkedNodes.append(j)

    return edges


if __name__ == "__main__":
    print("Acyclic:")
    aGraphAL = graph.Graph_AdjacencyList.GraphAdjacencyList()
    print("Number of edges:", generateAcyclicGraph(aGraphAL, 10))
    aGraphAL.print()
    aGraphIL = graph.Graph_IncidenceList.GraphIncidenceList()
    generateAcyclicGraph(aGraphIL, 10, True)
    aGraphIL.print()
    aGraphAM = graph.Graph_AdjacencyMatrix.GraphAdjacencyMatrix()
    generateAcyclicGraph(aGraphAM, 10)
    aGraphAM.print()

    print("Cyclic:")
    cGraphAL = graph.Graph_AdjacencyList.GraphAdjacencyList()
    print("Number of edges:", generateCyclicGraphNaive(cGraphAL, 10))
    cGraphAL.print()
    # cGraphIL = graph.Graph_IncidenceList.GraphIncidenceList()
    # generateCyclicGraphNaive(cGraphIL, 10, True)
    # cGraphIL.print()
    # cGraphAM = graph.Graph_AdjacencyMatrix.GraphAdjacencyMatrix()
    # generateCyclicGraphNaive(cGraphAM, 10)
    # cGraphAM.print()

    print("Random:")
    rGraphAL = graph.Graph_AdjacencyList.GraphAdjacencyList()
    print("Number of edges:", generateRandGraph(rGraphAL, 10))
    rGraphAL.print()

    print("Complete:")
    compGraphAL = graph.Graph_AdjacencyList.GraphAdjacencyList()
    print("Number of edges:", generateCompleteGraph(compGraphAL, 10))
    compGraphAL.print()
