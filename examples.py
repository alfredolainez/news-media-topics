from words_graph import SimpleGraphBuilder, NounPhraseGraphBuilder
from extractor import NewsScraper
import graph_cluster
import text_processing
import time
import community

from sklearn.preprocessing import scale
from sklearn.cluster import KMeans

def get_words_by_partition(partition):
    """
    Given a community partition of the form:
    { "word1": 2, "word2": 1, "word3": 1 .... }
    it returns the inverse dictionary:
    { 1: ["word1", "word3"], 2: ["word2"] .... }
    """
    words_by_part = {}
    for elem in partition:
        if partition[elem] not in words_by_part:
            words_by_part[partition[elem]] = [elem]
        else:
            words_by_part[partition[elem]].append(elem)

    return words_by_part

t0 = time.time()

news = NewsScraper('http://cnn.com', nthreads = 10)
news.pull()
news.scrape(200)
texts = (article['text'] for article in news.polished())

t1 = time.time()
print "Data retrieved in %.2f sec" %(t1-t0)

# Create a graph builder
gb = SimpleGraphBuilder(text_processing.clean_punctuation_and_stopwords)

gb.load_texts(texts)

# Show texts in the builder
# for text in texts:
#     print text
#     print "##################################################"
#
# print "##################################################"
# print  "TOKENIZED SENTENCES"
# print "##################################################"

# Show tokenized sentences
for text in gb.text_sentences[:1]:
    print "##################################################"
    for sentence in text:
        print sentence

# Building graph
G = gb.create_graph()
t2 = time.time()
print "Graph built in %.2f sec" %(t2-t1)

# Clustering
# ex = 2
# r = 2
# tol = 1e-3
# threshold = 1e-5
# M = graph_cluster.MCL_cluster(G,ex,r,tol,threshold)
# t3 = time.time()
# print "Graph clustered in %.2f sec" %(t3-t2)

partition = community.best_partition(G)

words_by_part = get_words_by_partition(partition)

# In order to get partitions in a given level of the dendogram (bigger level, smaller communities)
# although it seems that there are only usually 2 levels...
#dendogram = community.generate_dendogram(G)
#partition = community.partition_at_level(dendogram, 0)
#partition = community.partition_at_level(dendogram, 1)








# -- example using noun phrases
#
# gb = NounPhraseGraphBuilder(text_processing.clean_punctuation_and_stopwords)
# texts = (article['text'] for article in news.polished())
# gb.load_texts(texts)
# G = gb.create_graph(graphtype='occurence')
#
# partition = community.best_partition(G)
# words_by_part = get_words_by_partition(partition)
#
#
# for counter in xrange(0, len(words_by_part)):
# 	print '\nTopic {}:\n----------'.format(counter)
# 	H = G.subgraph(words_by_part[counter])
# 	print ', '.join(graph_cluster.pagerank_top_k(H, 10))

# -- example using non dictionary words

gb = SimpleGraphBuilder(text_processing.only_non_dictionary_words, stem_words=False)
texts = (article['text'] for article in news.polished())
gb.load_texts(texts)
G = gb.create_graph()

partition = community.best_partition(G)
words_by_part = get_words_by_partition(partition)

for counter in xrange(0, len(words_by_part)):
	print '\nTopic {}:\n----------'.format(counter)
	H = G.subgraph(words_by_part[counter])
	print ', '.join(graph_cluster.pagerank_top_k(H, 10))



# -- example using noun phrases

gb = NounPhraseGraphBuilder(text_processing.clean_punctuation_and_stopwords)
texts = (article['text'] for article in news.polished())
gb.load_texts(texts)
G = gb.create_graph(graphtype='occurence')

X = scale(graph_cluster.SpectralEmbedding(G, k = 20))
kmeans = KMeans(init='k-means++', n_clusters=20, n_init=10)

clusters = kmeans.fit_predict(X)

for cluster in set(clusters):
	print '\nTopic {}:\n----------'.format(cluster)
	nodes_in_cluster = np.array(G.nodes())[clusters == cluster]
	H = G.subgraph(nodes_in_cluster)
	# print ', '.join(graph_cluster.pagerank_top_k(H, 10))
	print ', '.join(pagerank_top_k(H, 10))



