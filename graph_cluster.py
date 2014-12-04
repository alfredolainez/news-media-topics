import networkx as nx
import numpy as np
from collections import defaultdict
from sklearn.preprocessing import normalize

# from scipy.linalg import eigh
from scipy.sparse.linalg import eigsh

def overlap_cluster(G, k, I, cliques=None):
    """
    Clusters G using the Clique Percolation Method
    
    Parameters
    ----------
    G : NetworkX graph
       Input graph
    k : int
       Size of smallest clique
    I : double 
       Intensity threshold for weighted graphs
       Set I=0 for unweighted graphs
    cliques: list or generator       
       Precomputed cliques (use networkx.find_cliques(G))
    Returns
    -------
    Yields sets of nodes, one for each k-clique community.
    """
    if k < 2:
        raise nx.NetworkXError("k=%d, k must be greater than 1."%k)
    if cliques is None:
        cliques = list(nx.find_cliques(G))
    cliques = [frozenset(c) for c in cliques if (len(c) >= k and _intensity(c,G) > I)]
    # First index which nodes are in which cliques
    membership_dict = defaultdict(list)
    for clique in cliques:
        for node in clique:
            membership_dict[node].append(clique)
    # For each clique, see which adjacent cliques percolate
    perc_graph = nx.Graph()
    perc_graph.add_nodes_from(cliques)
    for clique in cliques:
        for adj_clique in _get_adjacent_cliques(clique, membership_dict):
            if len(clique.intersection(adj_clique)) >= (k - 1):
                perc_graph.add_edge(clique, adj_clique)
                
    # Connected components of clique graph with perc edges
    # are the percolated cliques
    for component in nx.connected_components(perc_graph):
        yield(frozenset.union(*component))

def _intensity(clique, G):
    """
    For unweighted graphs, returns 1
    """
    product = 1.0
    k = 0    
    for edge in nx.subgraph(G,clique).edges():
        product *= G.get_edge_data(edge[0],edge[1])['weight']
        k += 1
    if product == 0:
        return 1
    else:
        return product**(1.0/k)


def _get_adjacent_cliques(clique, membership_dict):
    adjacent_cliques = set()
    for n in clique:
        for adj_clique in membership_dict[n]:
            if clique != adj_clique:
                adjacent_cliques.add(adj_clique)
    return adjacent_cliques

def pagerank_top_k(G, k = 10):
    pr = nx.pagerank_scipy(G)
    ky, v = pr.keys(), pr.values()
    ix = np.argsort(v)[::-1]
    return np.array(ky)[ix[:k]]

def SpectralEmbedding(G, k = 5):
    '''
    Takes a input Graph, and embeds it into k-dimensional
    euclidean space using a top-k-eigenvector embedding.
    '''

    # creates row normalized weight matrix
    M = normalize(nx.adj_matrix(G.copy()), norm='l1', axis=1)
    _, v = eigsh(M, k = k, which = 'LM')
    return v


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
    
    G = nx.fast_gnp_random_graph(40,.5)
    part = overlap_cluster(G,2,0)
    for p in part:
        print p
#    mat = np.array(nx.adj_matrix(G))
#    G = nx.fast_gnp_random_graph(40,.5)
#    mat[0,0] = 10
#    tol = 1e-5
#    threshold = 1e-5
#    ex = 2
#    r = 2
#    print mat
#    m = MCL_cluster(G,ex,r,tol,threshold)
#    print m