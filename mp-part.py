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
    return output_list

def monopolar_partition(input_graph):
    #initialization
    A_init = Graph() #an empty graph
    B_init = input_graph
    k = input_graph.number_of_nodes()
    Q = [[A_init,B_init],] # deliberately double-depth Q to manage 'branches'
    #loop body
    for branch in Q:
        A = branch.pop(0)
        print "A "
        print A.nodes()
        B = branch.pop()
        print "B "
        print B.nodes()
        if nx.number_of_nodes(A) > k:
            continue #reject branch

        p3s = forbidden_graphs(B)
        print "p3s "
        print p3s
        if p3s == []:
            return 'yes'
            break
        else:
            for vertex in p3s:
                # this decomposition is insufficient I need nx functions
                A_new = nx.union(A,nx.subgraph(input_graph,vertex))
                B_new = Graph(B)
                B_new.remove_node(vertex)
                Q.append([A_new,B_new])

        #all else fails
    return 'no'

def main():
    N = Graph()
    N.add_nodes_from([1,2,3,4])
    N.add_edges_from([(1,2),(2,3),(4,1)])
    Y = Graph()
    Y.add_nodes_from([1,2,3,4,5,6,7])
    Y.add_edges_from([(1,2),(2,3),(1,4),(4,3),(4,5),(4,6),(4,7),(1,3),(2,4)])
    print monopolar_partition(N)
    print monopolar_partition(Y)

if __name__ == '__main__':
    main()
