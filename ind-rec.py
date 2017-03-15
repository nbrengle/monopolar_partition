from networkx import Graph
import networkx as nx

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

    #This is only ensuring ACP is P3-free
    G = input_graph
    G_acp = G.subgraph(ACP)
    for u in ACP:
        u_neighbors = G_acp.neighbors(u)
        if DEBUG == True:
            print "u " + str(u)
            print u_neighbors
        for w in u_neighbors:
            w_neighbors = G_acp.neighbors(w)
            w_neighbors.remove(u) #remove bactrack
            if DEBUG == True:
                print "w " + str(w)
                print w_neighbors
            for x in w_neighbors:
                x_neighbors = G_acp.neighbors(x)
                x_neighbors.remove(w) #remove bactrack
                if DEBUG == True:
                    print "x " + str(x)
                    print x_neighbors
                if u not in x_neighbors:
                    reject_switch = 1
                    break

    if G.subgraph(BCP).edges() != []:
        if DEBUG == True:
            print "BCP had edges" + str(G.subgraph(BCP).edges())
        reject_switch = 1

    if reject_switch == 1:
        return 'reject'

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
            if w in AC_star: #? wrap in a Graph? THIS WON'T WORK
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
        u_prime_neighbors = G.subgraph(A_prime).neighbors(u) #A_prime probably has to become a graph first
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
        if rule_1 == "reject":
            if DEBUG == True:
                print "Reject Branch"
            break
        rule_2 = reduction_rule_5_2(G,constraint)
        if rule_2 != False:
            constraint = rule_2
            #if DEBUG == True:
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
        if reduction_loop == False:
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
            end_game = constraint
            continue
    #every branch is rejected
    #could make this more explicit by calling out an empty Q
    if end_game != False:
        return "Yes"
    else:
        return "No"

def main():
    #case1
    tri1 = nx.complete_graph(3)
    tri2 = nx.complete_graph(3)
    tri3 = nx.disjoint_union(tri1,tri2)
    tri3.add_edge(2,3)
    mp_tri3 = [[0,1,4,5],[2]]
    k_tri3 = 2
    v_tri3 = 3
    #print "tri3:2 " + str(inductive_recognition(tri3,v_tri3,mp_tri3,k_tri3))
    print "tri3:1 " + str(inductive_recognition(tri3,v_tri3,mp_tri3,1))

    G = Graph()
    G.add_nodes_from([1,2,3,4,5,6])
    G.add_edges_from([(1,2),(2,3),(3,4),(3,5),(3,6),(1,3)])
    mp_G = [[1,2],[4,5,6]]
    k_G = 1
    v_G = 3
    #print "G:1 " + str(inductive_recognition(G,v_G,mp_G,k_G))

    k5 = nx.complete_graph(5)
    k5.add_nodes_from([5,6,7])
    k5.add_edges_from([(4,5),(4,6),(4,7)])
    mp_k5 = [[0,1,2,3,],[5,6,7]]
    k_k5 = 1
    v_k5 = 4
    #print "k5:1 "+ str(inductive_recognition(k5,v_k5,mp_k5,k_k5))

if __name__ == '__main__':
    main()
