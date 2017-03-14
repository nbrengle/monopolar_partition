from networkx import Graph
import networkx as nx

def reduction_rule_5_1(constraint):
    '''
    If G[ACP] is not a cluster graph with at most k clusters,
    or if G[BCP] is not an edgeless graph,
    then reject the current constraint.
    '''
    pass
    if len(constraint) != 4:
        raise ValueError("A constraint is a 4-tuple")

def reduction_rule_5_2(constraint):
    '''
    If there is a vertex u ∈ BC∗ that has a neighbor in BCP,
    then set ACP ← ACP ∪ {u} and BC∗ ← BC∗ \ {u};
    ie: replace C with the constraint (AC∗, ACP ∪ {u}, BC∗ \ {u}, BCP)
    '''
    pass
    if len(constraint) != 4:
        raise ValueError("A constraint is a 4-tuple")

def reduction_rule_5_3(constraint):
    '''
    If there is a vertex u ∈ AC∗ and two vertices w, x ∈ ACP
    such that G[{u, w, x}] is a P3, set AC∗ ← AC∗ \ {u}
    and BCP ← BCP ∪ {u}.
    '''
    pass
    if len(constraint) != 4:
        raise ValueError("A constraint is a 4-tuple")

def branching_rule_5_1(constraint):
    '''
    If there are two vertices u, w ∈ AC∗ and a vertex x ∈ ACP
    such that G[{u, w, x}] is a P3, then branch into two branches:
    one associatedwith the constraint (AC∗ \ {u}, ACP, BC∗, BCP ∪ {u})
    and one associated with (AC∗ \ {w}, ACP, BC∗, BCP ∪ {w}).
    '''
    pass
    if len(constraint) != 4:
        raise ValueError("A constraint is a 4-tuple")

def branching_rule_5_2(constraint):
    '''
    If there is a vertex u ∈ AC∗such that {u} is a clusterin G[A'],
    then branch into two branches: the first is associated with the
    constraint (AC∗ \ {u}, ACP ∪ {u}, BC∗, BCP),
    and the second is associated with (AC∗ \ {u}, ACP, BC∗, BCP ∪ {u}).
    '''
    pass
    if len(constraint) != 4:
        raise ValueError("A constraint is a 4-tuple")

def inductive_recognition(input_graph,vertex,monopolar_partition,parameter):
    if len(monopolar_partition) != 2:
        raise ValueError("monopolar_partition must be of the form [A,B]")
    v = vertex
    k = parameter
    A_prime = monopolar_partition.pop(0) #set A
    B_prime = monopolar_partition.pop() #set B

    init_constraint_A = [A_prime, v, B_prime, []]
    init_constraint_B = [A_prime, [], B_prime, v]
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
    v = 2
    print inductive_recognition(tri3,v,mp,k)

if __name__ == '__main__':
    main()
