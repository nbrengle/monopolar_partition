from networkx import Graph
import networkx as nx

def forbidden_graphs(input_graph):
    #this will be an answer to the question:
    #does my neighbor have a neighbor?
    G = input_graph
    output_list = []
    #loop through all the nodes
    for node in nx.nodes_iter(G): #not sure I need an iter here
        for nbr in G.neighbors(node):
            if len(G.neighbors(nbr)) > 1:
                output_list.append(node)
                output_list.append(nbr)
                output_list.append(G.neighbors(nbr)[1])
        break
    #check if each node has a neighbor that has a neighbor
    # if that's true, grab all three and return them in a list
    return output_list

def monopolar_partition(input_graph, k):
    #initialization
    A_init = Graph() #an empty graph
    B_init = input_graph
    Q = [[A_init,B_init],] # deliberately double-depth Q to manage 'branches'
    #loop body
    for branch in Q:
        A = branch.popleft()
        B = branch.pop()
        if number_of_nodes(A) > k:
            continue #reject branch

        p3s = forbidden_graphs(B)
        if p3s == []: #this needs to change
            return 'yes'
            break
        else:
            for vertex in p3s:
                A_new = A.append(vertex)
                B_new = B.remove(vertex) # this decomposition isn't sufficient
                                         # we must also kill it off in every value
                                         # shit. some confusion here
                                         # B is a list of vertices not a graph
                Q.append([A_new,B_new])

        #all else fails
    return 'no'

def main():
    G = Graph()
    G.add_nodes_from([1,2,3,4])
    G.add_edges_from([(1,2),(2,3),(1,4)])
    print forbidden_graphs(G)

if __name__ == '__main__':
    main()
