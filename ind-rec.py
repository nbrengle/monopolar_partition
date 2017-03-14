from networkx import Graph
import networkx as nx

def detect_p3():
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

def reduction_rule_5_1(input_graph, constraint):
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If G[ACP] is not a cluster graph with at most k clusters,
    or if G[BCP] is not an edgeless graph,
    then reject the current constraint.
    '''
    if len(constraint) != 4:
        raise ValueError("A constraint must be a 4-tuple (AC_star, ACP, BC_star, BCP)")
    G = input_graph
    AC_star = constraint[0]
    ACP = constraint[1]
    BC_star = constraint[2]
    BCP = constraint[3]

    reject_switch = 0

    #still need to manage the check on ACP somehow...

    for vertex in BCP:
        if G.neighbors(vertex) != []:
            reject_switch = 1

    if reject_switch = 1:
        return 'reject'

def reduction_rule_5_2(input_graph, constraint):
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If there is a vertex u in BC_star that has a neighbor in BCP,
    then set ACP to ACP.union(u) and BC_star to BC_star.remove(u);
    ie: replace C with (AC_star, ACP.union(u), BC_star.remove(u), BCP)
    '''
    if len(constraint) != 4:
        raise ValueError("A constraint must be a 4-tuple (AC_star, ACP, BC_star, BCP)")
    G = input_graph
    AC_star = constraint[0]
    ACP = constraint[1]
    BC_star = constraint[2]
    BCP = constraint[3]

    for u in BC_star:
        for vertex in BCP:
            if u in G.neighbors(vertex):
                ACP.append(u) # as ACP is a list
                BC_star.remove(u) # as BC_star is a list

    return [AC_star,ACP,BC_star,BCP]


def reduction_rule_5_3(input_graph, constraint):
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If there is a vertex u in AC_star and two vertices w, x in ACP
    such that G[{u, w, x}] is a P3, set AC_star to AC_star.remove(u)
    and BCP to BCP.union(u).
    '''
    pass
    if len(constraint) != 4:
        raise ValueError("A constraint must be a 4-tuple (AC_star, ACP, BC_star, BCP)")
    G = input_graph
    AC_star = constraint[0]
    ACP = constraint[1]
    BC_star = constraint[2]
    BCP = constraint[3]

def branching_rule_5_1(input_graph, constraint):
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If there are two vertices u, w in AC_star and a vertex x in ACP
    such that G[{u, w, x}] is a P3, then branch into two branches:
    one with the constraint (AC_star.remove(u), ACP, BC_star, BCP.union(u))
    and one associated with (AC_star.remove(w), ACP, BC_star, BCP.union(w)).
    '''
    pass
    if len(constraint) != 4:
        raise ValueError("A constraint must be a 4-tuple (AC_star, ACP, BC_star, BCP)")
    G = input_graph
    AC_star = constraint[0]
    ACP = constraint[1]
    BC_star = constraint[2]
    BCP = constraint[3]

def branching_rule_5_2(input_graph, constraint):
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If there is a vertex u in AC_star such that u is a cluster in G[A_prime],
    then branch into two branches: the first is associated with the
    constraint (AC_star.remove(u), ACP.union(u), BC_star, BCP),
    and the second is with (AC_star.remove(u), ACP, BC_star, BCP.union(u)).
    '''
    pass
    if len(constraint) != 4:
        raise ValueError("A constraint must be a 4-tuple (AC_star, ACP, BC_star, BCP)")
    G = input_graph
    AC_star = constraint[0]
    ACP = constraint[1]
    BC_star = constraint [2]
    BCP = constraint[3]

def inductive_recognition(input_graph,vertex,monopolar_partition,parameter):
    if len(monopolar_partition) != 2:
        raise ValueError("monopolar_partition must be of the form [A,B]")
    v = vertex
    k = parameter
    A_prime = monopolar_partition.pop(0) #set A
    B_prime = monopolar_partition.pop() #set B

    init_constraint_A = [A_prime, [v,], B_prime, []]
    init_constraint_B = [A_prime, [], B_prime, [v,]]
    #reduction_rule_5_1
    #reduction_rule_5_2
    #reduction_rule_5_3
    #branching_rule_5_1
    #branching_rule_5_2

def main():
    tri1 = nx.complete_graph(3)
    tri2 = nx.complete_graph(3)
    tri3 = nx.disjoint_union(tri1,tri2)
    tri3.add_edge(2,3)
    mp = [[0,1,3,4,5],[2]]
    k = 2
    v = 3
    print inductive_recognition(tri3,v,mp,k)

if __name__ == '__main__':
    main()
