from networkx import Graph
import networkx as nx

def forbidden_graphs(input_graph):
    #this will be an answer to the question:
    #does my neighbor have a neighbor?
    G = input_graph
    output_list = []
    #loop through all the nodes
    for node in nx.nodes_iter(G): #not sure I need an iter here
        #print "node " + str(node)
        for nbr in G.neighbors(node):
            #print "nbr " + str(nbr)
            #print G.neighbors(nbr)
            if len(G.neighbors(nbr)) > 1:
                neighborsneighbors = G.neighbors(nbr)
                neighborsneighbors.remove(node)
                for nbrnbr in neighborsneighbors:
                    #print "nbrnbr " + str(nbrnbr)
                    #print G.neighbors(nbrnbr)
                    if node not in G.neighbors(nbrnbr):
                        output_list.append(node)
                        #print node
                        output_list.append(nbr)
                        #print nbr
                        output_list.append(G.neighbors(nbr)[1])
                        #print G.neighbors(nbr)[1]
                        break
                break
            if output_list != []:
                break
        if output_list != []:
            break
    return output_list

def monopolar_partition(input_graph, k):
    #initialization
    A_init = Graph() #an empty graph
    B_init = input_graph
    Q = [[A_init,B_init],] # deliberately double-depth Q to manage 'branches'
    #loop body
    for branch in Q:
        A = branch.pop(0)
        #print "A "
        #print A.nodes()
        B = branch.pop()
        #print "B "
        #print B.nodes()
        if nx.number_of_nodes(A) > k:
            continue #reject branch

        p3s = forbidden_graphs(B)
        #print "p3s "
        #print p3s
        if p3s == []:
            return 'yes'
            break
        else:
            for vertex in p3s:
                A_new = nx.union(A,nx.subgraph(input_graph,vertex))
                B_new = Graph(B)
                B_new.remove_node(vertex)
                Q.append([A_new,B_new])

        #all else fails
    return 'no'

def main():

    G = Graph()
    G.add_nodes_from([1,2,3,5,6,7])
    G.add_edges_from([(1,2),(2,3),(3,5),(3,6),(6,7),(1,3)])
    print "G:1 " + monopolar_partition(G,1)

    k5 = nx.complete_graph(5)
    G.add_nodes_from([5,6,7])
    G.add_edges_from([(4,5),(4,6),(4,7)])
    print "k5:1 "+ monopolar_partition(k5,1)

    tri1 = nx.complete_graph(3)
    tri2 = nx.complete_graph(3)
    tri3 = nx.disjoint_union(tri1,tri2)
    tri3.add_edge(2,3)
    #print tri3.nodes()
    #print tri3.edges()
    print "bowtie:1 " + monopolar_partition(tri3,1)
    print "bowtie:2 " + monopolar_partition(tri3,2)


if __name__ == '__main__':
    main()
