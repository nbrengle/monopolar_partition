import cProfile
from networkx import Graph
import networkx as nx
import time

def cluster_size(input_graph):
    '''
    This relies on the well known fact that
    "Every maximal independent set in a cluster graph chooses a single vertex
    from each cluster, so the size of such a set
    always equals the number of clusters" -- Wikipedia
    '''
    #calculate maximal IS
    #Initialize I to an empty set.
    G = input_graph
    I = []
    #While V is not empty:
    #Choose a node v in V;
    for v in G.nodes():
        #Add v to the set I;
        I.append(v)
        G.remove_node(v)#Remove from V the node v and all its neighbours.
    #Return I.
    return len(I)

def p3_free(input_graph):
    DEBUG = True
    G = input_graph
    for u in nx.nodes_iter(G):
        u_neighbors = G.neighbors(u)
        if DEBUG == True:
            print "u " + str(u)
            print u_neighbors
        for w in u_neighbors:
            w_neighbors = G.neighbors(w)
            w_neighbors.remove(u) #remove bactrack
            if DEBUG == True:
                print "w " + str(w)
                print w_neighbors
            for x in w_neighbors:
                x_neighbors = G.neighbors(x)
                x_neighbors.remove(w) #remove bactrack
                if DEBUG == True:
                    print "x " + str(x)
                    print x_neighbors
                if u not in x_neighbors:
                    return False
                    break
    return True

def valid_cluster_graph(input_graph, k):
    G = input_graph

    if not p3_free(G) or not cluster_size(G) <= k:
        return False
    else:
        return True

def reduction_rule_5_1(input_graph, constraint, k):
    DEBUG = True
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If G[ACP] is not a cluster graph with at most k clusters,
    or if G[BCP] is not an edgeless graph,
    then reject the current constraint.

    the graphs in A cannot contain an edgeless graph of order k + 1 as subgraph.
    In other words, every graph in A that has order at least k + 1 contains at
    least one edge.

    '''
    if DEBUG == True:
        print "Called reduction_rule_5_1"

    if len(constraint) != 4:
        raise ValueError("A constraint must be a 4-tuple (AC_star, ACP, BC_star, BCP)")
    G = input_graph
    AC_star = constraint[0]
    ACP = constraint[1]
    BC_star = constraint[2]
    BCP = constraint[3]

    if DEBUG == True:
        print "AC_star: " + str(AC_star)
        print "ACP: " + str(ACP)
        print "BC_star: " + str(BC_star)
        print "BCP: " + str(BCP)

    reject_switch = 0
    G = input_graph
    G_acp = G.subgraph(ACP)
    if not valid_cluster_graph(G_acp, k):
        return False

    if G.subgraph(BCP).edges() != []:
        if DEBUG == True:
            print "BCP had edges" + str(G.subgraph(BCP).edges())
        return False

    return True

def reduction_rule_5_2(input_graph, constraint):
    DEBUG = True
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If there is a vertex u in BC_star that has a neighbor in BCP,
    then set ACP to ACP.union(u) and BC_star to BC_star.remove(u);
    ie: replace C with (AC_star, ACP.union(u), BC_star.remove(u), BCP)
    '''
    if DEBUG == True:
        print "Called reduction_rule_5_2"

    if len(constraint) != 4:
        raise ValueError("A constraint must be a 4-tuple (AC_star, ACP, BC_star, BCP)")
    G = input_graph
    AC_star = constraint[0]
    ACP = constraint[1]
    BC_star = constraint[2]
    BCP = constraint[3]

    if DEBUG == True:
        print "AC_star: " + str(AC_star)
        print "ACP: " + str(ACP)
        print "BC_star: " + str(BC_star)
        print "BCP: " + str(BCP)

    for u in BC_star:
        if DEBUG == True:
            print "u: " + str(u)
        for vertex in BCP:
            if DEBUG == True:
                print "vertex: " + str(vertex)
            if u in G.neighbors(vertex):
                ACP.append(u) # as ACP is a list
                BC_star.remove(u) # as BC_star is a list
                if DEBUG == True:
                    print [AC_star,ACP,BC_star,BCP]
                return [AC_star,ACP,BC_star,BCP]
    if DEBUG == True:
        print "rule 2 fell through to false"
    return False

def reduction_rule_5_3(input_graph, constraint):
    DEBUG = True
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If there is a vertex u in AC_star and two vertices w, x in ACP
    such that G[{u, w, x}] is a P3, set AC_star to AC_star.remove(u)
    and BCP to BCP.union(u).
    '''
    if DEBUG == True:
        print "Called reduction_rule_5_3"

    if len(constraint) != 4:
        raise ValueError("A constraint must be a 4-tuple (AC_star, ACP, BC_star, BCP)")
    G = input_graph
    AC_star = constraint[0]
    ACP = constraint[1]
    BC_star = constraint[2]
    BCP = constraint[3]

    if DEBUG == True:
        print "AC_star: " + str(AC_star)
        print "ACP: " + str(ACP)
        print "BC_star: " + str(BC_star)
        print "BCP: " + str(BCP)

    G = input_graph
    for u in AC_star:
        u_neighbors = G.neighbors(u)
        if DEBUG == True:
            print "u " + str(u)
            print "u_neighbors " + str(u_neighbors)
        for w in u_neighbors:
            if w in ACP: #? wrap in a Graph? THIS WON'T
                w_neighbors = G.neighbors(w)
                w_neighbors.remove(u) #remove bactrack
                if DEBUG == True:
                    print "w " + str(w)
                    print "w_neighbors " + str(w_neighbors)
                for x in w_neighbors:
                    if x in ACP: #? wrap in a Graph? THIS WON'T WORK
                        x_neighbors = G.neighbors(x)
                        x_neighbors.remove(w) #remove bactrack
                        if DEBUG == True:
                            print "x " + str(x)
                            print "x_neighbors " + str(x_neighbors)
                        if u not in x_neighbors:
                            AC_star.remove(u) #is list
                            BCP.append(u) #is list
                            return [AC_star,ACP,BC_star,BCP]
    if DEBUG == True:
        print "rule 3 fell through to false"
    return False

def branching_rule_5_1(input_graph, constraint):
    DEBUG = True
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If there are two vertices u, w in AC_star and a vertex x in ACP
    such that G[{u, w, x}] is a P3, then branch into two branches:
    one with the constraint (AC_star.remove(u), ACP, BC_star, BCP.union(u))
    and one associated with (AC_star.remove(w), ACP, BC_star, BCP.union(w)).
    '''
    if DEBUG == True:
        print "Called branching_rule_5_1"

    if len(constraint) != 4:
        raise ValueError("A constraint must be a 4-tuple (AC_star, ACP, BC_star, BCP)")
    G = input_graph
    AC_star = constraint[0]
    ACP = constraint[1]
    BC_star = constraint[2]
    BCP = constraint[3]

    if DEBUG == True:
        print "AC_star: " + str(AC_star)
        print "ACP: " + str(ACP)
        print "BC_star: " + str(BC_star)
        print "BCP: " + str(BCP)

    G = input_graph
    for u in AC_star:
        u_neighbors = G.neighbors(u)
        if DEBUG == True:
            print "u " + str(u)
            print "u_neighbors " + str(u_neighbors)
        for w in u_neighbors:
            if w in AC_star:
                w_neighbors = G.neighbors(w)
                w_neighbors.remove(u) #remove bactrack
                if DEBUG == True:
                    print "w " + str(w)
                    print "w_neighbors " + str(w_neighbors)
                for x in w_neighbors:
                    if x in ACP:
                        x_neighbors = G.neighbors(x)
                        x_neighbors.remove(w) #remove bactrack
                        if DEBUG == True:
                            print "x " + str(x)
                            print "x_neighbors " + str(x_neighbors)
                        if u not in x_neighbors:
                            AC_star_1 = list(AC_star)
                            AC_star_1.remove(u)
                            AC_star_2 = list(AC_star)
                            AC_star_2.remove(w)
                            BCP_1 = list(BCP)
                            BCP_1.append(u)
                            BCP_2 = list(BCP)
                            BCP_2.append(w)
                            if DEBUG == True:
                                print str([
                                        [AC_star_1,ACP,BC_star,BCP_1],
                                        [AC_star_2,ACP,BC_star,BCP_2],
                                        ])
                            return [
                                    [AC_star_1,ACP,BC_star,BCP_1],
                                    [AC_star_2,ACP,BC_star,BCP_2],
                                    ]
    if DEBUG == True:
        print "branch 1 fell through to false"
    return False

def branching_rule_5_2(input_graph, constraint, A_prime):
    DEBUG = True
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If there is a vertex u in AC_star such that u is a cluster in G[A_prime],
    then branch into two branches: the first is associated with the
    constraint (AC_star.remove(u), ACP.union(u), BC_star, BCP),
    and the second is with (AC_star.remove(u), ACP, BC_star, BCP.union(u)).
    '''
    if DEBUG == True:
        print "Called branching_rule_5_2"

    if len(constraint) != 4:
        raise ValueError("A constraint must be a 4-tuple (AC_star, ACP, BC_star, BCP)")
    G = input_graph
    AC_star = constraint[0]
    ACP = constraint[1]
    BC_star = constraint [2]
    BCP = constraint[3]

    if DEBUG == True:
        print "AC_star: " + str(AC_star)
        print "ACP: " + str(ACP)
        print "BC_star: " + str(BC_star)
        print "BCP: " + str(BCP)

    #if u has only 1 edge, it's likely a singleton cluster
    #this... might not work
    for u in AC_star:
        u_prime_neighbors = G.subgraph(A_prime).neighbors(u)
        if DEBUG == True:
            print "u: " + str(u)
            print u_prime_neighbors
        if len(u_prime_neighbors) > 1:
            AC_star_no_u = list(AC_star)
            AC_star_no_u.remove(u)
            ACP_u = list(ACP)
            ACP_u.append(u)
            BCP_u = list(BCP)
            BCP_u.append(u)
            if DEBUG == True:
                print   str([
                        [AC_star_no_u,ACP_u,BC_star,BCP],
                        [AC_star_no_u,ACP,BC_star,BCP_u],
                        ])
            return  [
                    [AC_star_no_u,ACP_u,BC_star,BCP],
                    [AC_star_no_u,ACP,BC_star,BCP_u],
                    ]
    if DEBUG == True:
        print "branch 2 fell through to false"
    return False

def reduction_rule_loop(G, branch, k):
    DEBUG = True
    constraint = branch
    goto = True
    while goto == True:
        rule_1 = reduction_rule_5_1(G,constraint,k)
        if not rule_1:
            if DEBUG == True:
                print "Reject Branch"
            break
        rule_2 = reduction_rule_5_2(G,constraint)
        if rule_2 != False:
            constraint = rule_2
            if DEBUG == True:
                print "rule_2: " + str(rule_2)
            continue
        rule_3 = reduction_rule_5_3(G,constraint)
        if rule_3 != False:
            constraint = rule_3
            if DEBUG == True:
                print "rule_3: " + str(rule_3)
            continue
        if rule_3 == False: #I think this works, it's a bit weird
            return constraint
            goto = False
    return False

def inductive_recognition(input_graph,vertex,monopolar_partition,parameter):
    DEBUG = True

    if len(monopolar_partition) != 2:
        raise ValueError("monopolar_partition must be of the form [A,B]")
    v = vertex
    k = parameter
    G = input_graph
    A_prime = monopolar_partition[0] #set A
    B_prime = monopolar_partition[1] #set B

    init_constraint_A = [A_prime, [v,], B_prime, []]
    init_constraint_B = [A_prime, [], B_prime, [v,]]

    #Going to use a Queue here instead of a formal tree, sufficient w/o parallel
    Q = [init_constraint_A,init_constraint_B]
    end_game = False

    for branch in Q:
        if DEBUG == True:
            print "branch: " + str(branch)
        reduction_loop = reduction_rule_loop(G, branch, k)
        if not reduction_loop:
            continue
        else:
            constraint = reduction_loop
            b_rule_1 = branching_rule_5_1(G,constraint)
            if b_rule_1 != False:
                for new_branch in b_rule_1:
                    Q.append(new_branch)
            b_rule_2 = branching_rule_5_2(G,constraint,A_prime)
            if b_rule_2 != False:
                for new_branch in b_rule_2:
                    Q.append(new_branch)
            A = nx.union(G.subgraph(constraint[0]),G.subgraph(constraint[2]))
            end_game = valid_cluster_graph(A, k)
            continue
    #every branch is rejected
    #could make this more explicit by calling out an empty Q
    return end_game

def case_bowtie(desired_runs,repetitions):
    tri1 = nx.complete_graph(3)
    tri2 = nx.complete_graph(3)
    tri3 = nx.disjoint_union(tri1,tri2)
    tri3.add_edge(2,3)
    mp_tri3 = [[0,1,4,5],[2]]
    k_tri3 = 1
    v_tri3 = 3

    average_times = []
    for x in range(0, repetitions):
        start_time = time.time()
        for n in range(0, desired_runs):
            print inductive_recognition(tri3,v_tri3,mp_tri3,k_tri3) #rm-print
        elapsed_time = time.time() - start_time

        average_time = elapsed_time / desired_runs
        average_times.append(average_time)

    return min(average_times)

def case_k3_plus_claw(desired_runs,repetitions):
    G = Graph()
    G.add_nodes_from([1,2,3,4,5,6])
    G.add_edges_from([(1,2),(2,3),(3,4),(3,5),(3,6),(1,3)])
    mp_G = [[1,2],[4,5,6]]
    k_G = 1
    v_G = 3

    average_times = []
    for x in range(0, repetitions):
        start_time = time.time()
        for n in range(0, desired_runs):
            print inductive_recognition(G,v_G,mp_G,k_G) #rm-print
        elapsed_time = time.time() - start_time

        average_time = elapsed_time / desired_runs
        average_times.append(average_time)

    return min(average_times)

def case_k5_plus_claw(desired_runs,repetitions):
    k5 = nx.complete_graph(5)
    k5.add_nodes_from([5,6,7])
    k5.add_edges_from([(4,5),(4,6),(4,7)])
    mp_k5 = [[0,1,2,3,],[5,6,7]]
    k_k5 = 1
    v_k5 = 4

    average_times = []
    for x in range(0, repetitions):
        start_time = time.time()
        for n in range(0, desired_runs):
            print inductive_recognition(k5,v_k5,mp_k5,k_k5) #rm-print
        elapsed_time = time.time() - start_time

        average_time = elapsed_time / desired_runs
        average_times.append(average_time)

    return min(average_times)

def case_from_3_1(desired_runs,repetitions):
    G = Graph()
    G.add_nodes_from([1,2,3,4,5,6,7,8,9,10])
    G.add_edges_from([(1,2),(2,3),(2,4),(2,5),(3,5),(3,4),(4,6),(6,7),(7,10),(7,9),(7,8),(8,9),(9,10)])
    mp = [[2,3,5,6,9,10],[1,4,8]]
    k = 2
    v = 7

    average_times = []
    for x in range(0, repetitions):
        start_time = time.time()
        for n in range(0, desired_runs):
            print inductive_recognition(G,v,mp,k) #rm-print
        elapsed_time = time.time() - start_time

        average_time = elapsed_time / desired_runs
        average_times.append(average_time)

    return min(average_times)

def case_on_20(desired_runs,repetitions):
    G = Graph()
    G.add_nodes_from([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    G.add_edges_from([(1,6),(1,4),(2,7),(3,8),(3,9),(3,4),(3,13),(4,14),(4,5),(5,10),
                      (6,12),(7,8),(8,9),(8,13),(9,13),(9,14),(10,14),(11,5),(11,15),
                      (10,15),(10,11),(5,15),(14,18),(14,19),(15,19),(15,20),(17,18),
                      (12,17),(12,18),(19,20)])
    mp = [[1,2,3,5,8,9,10,11,12,13,17,18,19,20],[4,6,7,15,16]]
    k = 6
    v = 14

    average_times = []
    for x in range(0, repetitions):
        start_time = time.time()
        for n in range(0, desired_runs):
            print inductive_recognition(G,v,mp,k) #rm-print
        elapsed_time = time.time() - start_time

        average_time = elapsed_time / desired_runs
        average_times.append(average_time)

    return min(average_times)

def main():
    #cProfile.run('case_bowtie()')
    #print "case_bowtie " + str(case_bowtie(1,1))
    print "case_k3_plus_claw " + str(case_k3_plus_claw(1,1))
    #print "case_k5_plus_claw " + str(case_k5_plus_claw(1,1))
    #print "case_from_3_1 " + str(case_from_3_1(1,1))
    #print "case_on_20 " + str(case_on_20(1,1))

if __name__ == '__main__':
    main()
