import networkx as nx
import numpy as np

def MCL_cluster(G,ex,r,tol,threshold):
    """
    Computes a clustering of graph G using the MCL algorithm 
    with power parameter ex and inflation parameter r
    The algorithm runs until the relative decrease in norm 
    is lower than tol or after 10,000 iterations
    Returns an array whose values are greater than threshold
    Leaves the graph G unchanged
    """

    M = np.array(nx.adj_matrix(G.copy()))
    M = inflate(M,1)

    norm_old = 0
    norm_new = np.linalg.norm(M)
    it = -1
    itermax = 10000
    while it < itermax:
        it += 1
        norm_old = norm_new
        M = M**ex
        M = inflate(M,r)
        norm_new = np.linalg.norm(M)
        if __name__ == '__main__':
            # debugging
            print "iteration %s" %it
            print "prop. decrease %s" %(abs(norm_old-norm_new)/norm_old)
        if abs(norm_old-norm_new)/norm_old < tol:
            print it
            break
    M[M < threshold] = 0
    return M

def inflate(M,r):
    """
    Returns a copy of the numpy array M inflated columnwise by a factor r
    Rmk: r = 1 makes M stochastic
    """
    col_sums = np.power(M,r).sum(axis=0)
    mat = np.power(M,r) / col_sums[np.newaxis,:]
    return mat

def add_self_loops(G):
    """
    Adds self loops of weight 1 to the weighted graph G (in place)
    for nodes that don't have one already
    """
    for node in G.nodes():
        if not G.has_edge(node, node):
            G.add_edge(node, node, weight=1.)
            
if __name__ == '__main__':
    """ 
    debugging  code
    """
    G = nx.Graph()
    L = ['a','b','c','d']
    G.add_nodes_from(L)
    G.add_weighted_edges_from([('a','b',1),('c','b',2),('c','a',1),('d','a',1)])
    mat = np.array(nx.adj_matrix(G))
#    G = nx.fast_gnp_random_graph(40,.5)
#    mat[0,0] = 10
    tol = 1e-5
    threshold = 1e-5
    ex = 2
    r = 2
    print mat
    m = MCL_cluster(G,ex,r,tol,threshold)
    print m