import cProfile
from networkx import Graph
import networkx as nx
import time

def forbidden_graphs(input_graph):
    DEBUG = False
    '''
    B should be an Independent Set and have no edges
    '''
    G = input_graph
    if DEBUG==True:
        print "Edges in B "
        print G.edges()
    return G.edges()

def monopolar_partition(input_graph, k):
    DEBUG = False
    #initialization
    G = input_graph
    A_init = Graph() #an empty graph
    B_init = input_graph
    Q = [[A_init,B_init],] # deliberately double-depth Q to manage 'branches'
    #loop body
    for branch in Q:
        A = branch[0]
        if DEBUG == True:
            print "A "
            print A.nodes()
        B = branch[1]
        if DEBUG == True:
            print "B "
            print B.nodes()
        if nx.number_of_nodes(A) > k:
            continue #reject branch

        p2s = forbidden_graphs(B)
        if DEBUG == True:
            print "p2s "
            print p2s
        if p2s == []:
            return True
            break
        else:
            p2s = p2s[0]
            for vertex in p2s:
                A_new = nx.union(A,nx.subgraph(input_graph,vertex))
                B_new = Graph(B)
                B_new.remove_node(vertex)
                Q.append([A_new,B_new])

        #all else fails
    return False

def case_bowtie(desired_runs,repetitions,k):
    tri1 = nx.complete_graph(3)
    tri2 = nx.complete_graph(3)
    tri3 = nx.disjoint_union(tri1,tri2)
    tri3.add_edge(2,3)
    k_tri3 = k

    average_times = []
    for x in range(0, repetitions):
        start_time = time.time()
        for n in range(0, desired_runs):
            monopolar_partition(tri3,k_tri3)
        elapsed_time = time.time() - start_time

        average_time = elapsed_time / desired_runs
        average_times.append(average_time)

    print monopolar_partition(tri3,k_tri3)
    return min(average_times)

def case_k3_plus_claw(desired_runs,repetitions,k):
    G = Graph()
    G.add_nodes_from([1,2,3,4,5,6])
    G.add_edges_from([(1,2),(2,3),(3,4),(3,5),(3,6),(1,3)])
    k_G = k

    average_times = []
    for x in range(0, repetitions):
        start_time = time.time()
        for n in range(0, desired_runs):
            monopolar_partition(G,k_G)
        elapsed_time = time.time() - start_time

        average_time = elapsed_time / desired_runs
        average_times.append(average_time)

    print monopolar_partition(G,k_G)
    return min(average_times)

def case_k5_plus_claw(desired_runs,repetitions,k):
    k5 = nx.complete_graph(5)
    k5.add_nodes_from([5,6,7])
    k5.add_edges_from([(4,5),(4,6),(4,7)])
    k_k5 = k

    average_times = []
    for x in range(0, repetitions):
        start_time = time.time()
        for n in range(0, desired_runs):
            monopolar_partition(k5,k_k5)
        elapsed_time = time.time() - start_time

        average_time = elapsed_time / desired_runs
        average_times.append(average_time)

    print monopolar_partition(k5,k_k5)
    return min(average_times)

def case_from_3_1(desired_runs,repetitions,k):
    G = Graph()
    G.add_nodes_from([1,2,3,4,5,6,7,8,9,10])
    G.add_edges_from([(1,2),(2,3),(2,4),(2,5),(3,5),(3,4),(4,6),(6,7),
                      (7,10),(7,9),(7,8),(8,9),(9,10)])

    average_times = []
    for x in range(0, repetitions):
        start_time = time.time()
        for n in range(0, desired_runs):
            monopolar_partition(G,k)
        elapsed_time = time.time() - start_time

        average_time = elapsed_time / desired_runs
        average_times.append(average_time)

    print monopolar_partition(G,k)
    return min(average_times)

def case_on_20(desired_runs,repetitions,k):
    G = Graph()
    G.add_nodes_from([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    G.add_edges_from([(1,6),(1,4),(2,7),(3,8),(3,9),(3,4),(3,13),(4,14),(4,5),
                      (5,10),(6,12),(7,8),(8,9),(8,13),(9,13),(9,14),(10,14),
                      (11,5),(11,15),(10,15),(10,11),(5,15),(14,18),(14,19),
                      (15,19),(15,20),(17,18),(12,17),(12,18),(19,20)])

    average_times = []
    for x in range(0, repetitions):
        start_time = time.time()
        for n in range(0, desired_runs):
            monopolar_partition(G,k)
        elapsed_time = time.time() - start_time

        average_time = elapsed_time / desired_runs
        average_times.append(average_time)

    print monopolar_partition(G,k)
    return min(average_times)

def main():
    cProfile.run('case_bowtie(100,3,1)')
    print "case_bowtie " + str(case_bowtie(100,3,2))
    print "case_bowtie " + str(case_bowtie(100,3,3))
    print "case_bowtie " + str(case_bowtie(100,3,5))
    cProfile.run('case_k3_plus_claw(100,3,1)')
    print "case_k3_plus_claw " + str(case_k3_plus_claw(100,3,2))
    print "case_k3_plus_claw " + str(case_k3_plus_claw(100,3,3))
    print "case_k3_plus_claw " + str(case_k3_plus_claw(100,3,5))
    cProfile.run('case_k5_plus_claw(100,3,1)')
    print "case_k5_plus_claw " + str(case_k5_plus_claw(100,3,2))
    print "case_k5_plus_claw " + str(case_k5_plus_claw(100,3,4))
    print "case_k5_plus_claw " + str(case_k5_plus_claw(100,3,6))
    cProfile.run('case_from_3_1(100,3,2)')
    print "case_from_3_1 " + str(case_from_3_1(100,3,2))
    print "case_from_3_1 " + str(case_from_3_1(100,3,5))
    print "case_from_3_1 " + str(case_from_3_1(100,3,7))
    cProfile.run('case_on_20(100,3,6)')
    print "case_on_20 " + str(case_on_20(100,3,5))
    print "case_on_20 " + str(case_on_20(100,3,10))
    print "case_on_20 " + str(case_on_20(100,3,15))


if __name__ == '__main__':
    main()
