from networkx import Graph
import networkx as nx

def forbidden_graphs(input_graph):
    '''
    There's a p3 if:
        my neighbor(1) has a neighbor(2) that is not me
        neighbor(2) has a neighbor(3) that is not me
    '''
    DEBUG = True
    output_list = []
    G = input_graph
    for n_0 in nx.nodes_iter(G):
        neighbors_1 = G.neighbors(n_0)

        if DEBUG==True:
            print "n_0 " + str(n_0)
            print "neighbors_1" + str(neighbors_1)

        for n_1 in neighbors_1:
            neighbors_2 = G.neighbors(n_1)
            neighbors_2.remove(n_0) #remove bactrack

            if DEBUG==True:
                print "n_1 " + str(n_1)
                print "neighbors_2" + str(neighbors_2)

            for n_2 in neighbors_2:
                neighbors_3 = G.neighbors(n_2)
                neighbors_3.remove(n_1) #remove bactrack
                if DEBUG==True:
                    print "n_2 " + str(n_2)
                    print "neighbors_3_mod" + str(neighbors_3)

                if n_0 not in neighbors_3:
                    output_list.append(n_0)
                    output_list.append(n_1)
                    output_list.append(n_2)
                    if DEBUG==True:
                        print output_list
                    return output_list
    return output_list

def monopolar_partition(input_graph, k):
    DEBUG = True
    #initialization
    A_init = Graph() #an empty graph
    B_init = input_graph
    Q = [[A_init,B_init],] # deliberately double-depth Q to manage 'branches'
    #loop body
    for branch in Q:
        A = branch.pop(0)
        if DEBUG==True:
            print "A "
            print A.nodes()
        B = branch.pop()
        if DEBUG==True:
            print "B "
            print B.nodes()
        if nx.number_of_nodes(A) > k:
            continue #reject branch

        p3s = forbidden_graphs(B)
        if DEBUG==True:
            print "p3s "
            print p3s
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
    #print "G:1 " + monopolar_partition(G,1)

    k5 = nx.complete_graph(5)
    G.add_nodes_from([5,6,7])
    G.add_edges_from([(4,5),(4,6),(4,7)])
    #print "k5:1 "+ monopolar_partition(k5,1)

    tri1 = nx.complete_graph(3)
    tri2 = nx.complete_graph(3)
    tri3 = nx.disjoint_union(tri1,tri2)
    tri3.add_edge(2,3)
    #print tri3.nodes()
    #print tri3.edges()
    print "bowtie:1 " + monopolar_partition(tri3,1)
    #print "bowtie:2 " + monopolar_partition(tri3,2)


if __name__ == '__main__':
    main()
