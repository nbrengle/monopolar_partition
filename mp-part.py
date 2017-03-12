import argparse


###
# graphs will be dictionaries with lists of vertices
#     graph = {'A': ['B', 'C'],
#             'B': ['C', 'D'],
#             'C': ['D'],
#             'D': ['C'],
#             'E': ['F'],
#             'F': ['C']}
###

def forbidden_graphs(vertices):
    #this will be an answer to the question:
    #does my neighbor have a neighbor?

    #we have to iterate through each vertex in the lists
    #but fuck, if this is just a list we can't do real partitions
    #because there's no decomposition of the actual graph
    #we might need a more intelligent structure here fuck


def monopolar_partition(graph, k):
    #initialization
    A_init = []
    B_init = graph.keys
    Q = [[A_init,B_init],] # deliberately double-depth Q to manage 'branches'
    #loop body
    for branch in Q:
        A = branch.popleft()
        B = branch.pop()
        if len(A) > k:
            continue #reject branch

        p3s = forbidden_graphs(B)
        if p3s == []:
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
    parser = argparse.ArgumentParser()
    parser.add_argument(graph)
    parser.add_argument(k)
    args = parser.parse_args()

    monopolar_partition(args.graph)

if __name__ == '__main__':
    main()
