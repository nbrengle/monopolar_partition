from networkx import Graph
import networkx as nx

def reduction_rule_5_1(input_graph, constraint, k):
    DEBUG = False
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If G[ACP] is not a cluster graph with at most k clusters,
    or if G[BCP] is not an edgeless graph,
    then reject the current constraint.
    '''
    #if DEBUG == True:
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
    #the number of clusters is not addressed
    G = input_graph
    for u in ACP:
        u_neighbors = G.subgraph(ACP).neighbors(u)
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
                    reject_switch = 1
                    break

    for vertex in BCP:
        if G.neighbors(vertex) != []:
            reject_switch = 1
            break

    if reject_switch == 1:
        return 'reject'

def reduction_rule_5_2(input_graph, constraint):
    DEBUG = False
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If there is a vertex u in BC_star that has a neighbor in BCP,
    then set ACP to ACP.union(u) and BC_star to BC_star.remove(u);
    ie: replace C with (AC_star, ACP.union(u), BC_star.remove(u), BCP)
    '''
    #if DEBUG == True:
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
        for vertex in BCP:
            if u in G.neighbors(vertex):
                ACP.append(u) # as ACP is a list
                BC_star.remove(u) # as BC_star is a list
                if DEBUG == True:
                    print [AC_star,ACP,BC_star,BCP]
                return [AC_star,ACP,BC_star,BCP]
    return False

def reduction_rule_5_3(input_graph, constraint):
    DEBUG = False
    '''
    Constraint should be of the form: (AC_star, ACP, BC_star, BCP)

    If there is a vertex u in AC_star and two vertices w, x in ACP
    such that G[{u, w, x}] is a P3, set AC_star to AC_star.remove(u)
    and BCP to BCP.union(u).
    '''
    #if DEBUG == True:
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
        for w in u_neighbors:
            if w in ACP: #? wrap in a Graph? THIS WON'T
                w_neighbors = G.neighbors(w)
                w_neighbors.remove(u) #remove bactrack
                for x in w_neighbors:
                    if x in ACP: #? wrap in a Graph? THIS WON'T WORK
                        x_neighbors = G.neighbors(x)
                        x_neighbors.remove(w) #remove bactrack
                        if u not in x_neighbors:
                            AC_star.remove(u) #is list
                            BCP.append(u) #is list
                            return [AC_star,ACP,BC_star,BCP]
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
        for w in u_neighbors:
            if w in AC_star: #? wrap in a Graph? THIS WON'T WORK
                w_neighbors = G.neighbors(w)
                w_neighbors.remove(u) #remove bactrack
                for x in w_neighbors:
                    if x in ACP: #? wrap in a Graph? THIS WON'T WORK
                        x_neighbors = G.neighbors(x)
                        x_neighbors.remove(w) #remove bactrack
                        if u not in x_neighbors:
                            AC_star_1 = list(AC_star)
                            AC_star_2 = list(AC_star)
                            BCP_1 = list(BCP)
                            BCP_2 = list(BCP)
                            return [
                                    [AC_star_1.remove(u),ACP,BC_star,BCP_1.append(u)],
                                    [AC_star_2.remove(w),ACP,BC_star,BCP_2.append(w)],
                                    ]
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
        if len(u_prime_neighbors) > 1:
            AC_star_no_u = list(AC_star)
            AC_star_no_u.remove(u)
            ACP_u = list(ACP)
            ACP_u.append(u)
            BCP_u = list(BCP)
            BCP_u.append(u)
            return  [
                    [AC_star_no_u,ACP_u,BC_star,BCP],
                    [AC_star_no_u,ACP,BC_star,BCP_u],
                    ]
    return False

def reduction_rule_loop(G, branch, k):
    constraint = branch
    goto = True
    while goto == True:
        rule_1 = reduction_rule_5_1(G,constraint,k)
        if rule_1 == "reject":
            print "About to break"
            break
        rule_2 = reduction_rule_5_2(G,constraint)
        if rule_2 != False:
            constraint = rule_2
            continue
        rule_3 = reduction_rule_5_3(G,constraint)
        if rule_3 != False:
            constraint = rule_3
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
    if DEBUG == True:
        print "init_constraint_A" + str(init_constraint_A)
        print "init_constraint_B" + str(init_constraint_B)

    #Going to use a Queue here instead of a formal tree, sufficient w/o parallel
    Q = [init_constraint_A,init_constraint_B]
    print Q
    end_game = False
    for branch in Q:
        #if reduction rule 5.1 returns reject, we toss this branch
        #otherwise we try 5.2 then 5.3
        #if a reduction rule succeeds, we jump back to 1
        #if none of the reduction rules apply, we try the branching rule

        #branching rules return a tuple of constraints to be added to the Q
        #or an indicator that the branching rule doesn't apply: False
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
                    Q.insert(0, new_branch)
            b_rule_2 = branching_rule_5_2(G,constraint,A_prime)
            if b_rule_2 != False:
                for new_branch in b_rule_2:
                    Q.insert(0, new_branch)
            if b_rule_2 == False:
                print Q
                end_game = constraint
                print end_game
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
    mp_tri3 = [[0,1,2],[4,5]]
    k_tri3 = 2
    v_tri3 = 3
    print "tri3:2 " + str(inductive_recognition(tri3,v_tri3,mp_tri3,k_tri3))
    #print "tri3:1 " + str(inductive_recognition(tri3,v_tri3,mp_tri3,1))

if __name__ == '__main__':
    main()
