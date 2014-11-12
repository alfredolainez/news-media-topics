import networkx as nx
import numpy as np

def MCL_cluster(G,ex,r,tol):
    """
    Computes a clustering of graph G using the MCL algorithm 
    with power parameter ex and inflation parameter r
    The algorithm runs until the relative decrease in norm 
    is lower than tol or after 10,000 iterations    
    Leaves the graph G unchanged
    """

    M = nx.adj_matrix(G.copy())
    inflate(M,1)

    norm_old = 0
    norm_new = np.linalg.norm(M)
    it = -1
    itermax = 10000
    while it < itermax:
        it += 1
        norm_old = norm_new
        M = M**ex
        inflate(M,r)
        norm_new = np.linalg.norm(M)
        print "iteration %s" %it
        print "prop. decrease %s" %(abs(norm_old-norm_new)/norm_old)
        if abs(norm_old-norm_new)/norm_old < tol:
            print it
            break
    return M

def inflate(M,r):
    """
    Inflates the numpy matrix M columnwise by a factor r (in place)
    Rmk: r = 1 makes M stochastic
    """
    for j in range(M.shape[1]):
        col_sum = sum( [x**r for x in M[:,j]] )
        for i in range(M.shape[0]):
            M[i,j] = M[i,j]**r/col_sum
    return 

def add_self_loops(G):
    """
    Adds self loops of weight 1 to the weighted graph G (in place)
    for nodes that don't have one already
    """
    for node in G.nodes():
        if not G.has_edge(node, node):
            G.add_edge(node, node, weight=1.)

""" testing """
#G = nx.Graph()
#L = ['a','b','c','d']
#G.add_nodes_from(L)
#G.add_weighted_edges_from([('a','b',1),('c','b',2),('c','a',1),('d','a',1)])
G = nx.fast_gnp_random_graph(5,.9)
mat = nx.adj_matrix(G)
tol = 0.000001
ex = 2
r = 2
print MCL_cluster(G,ex,r,tol)