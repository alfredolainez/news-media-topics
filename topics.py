from words_graph import SimpleGraphBuilder, NounPhraseGraphBuilder
from extractor import NewsScraper
import graph_cluster
import text_processing
import time
import community
import networkx as nx
import matplotlib.pyplot as plt

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

def get_news(url, number):
    """
    Retrieves news from the specified source
    """

    t0 = time.time()
    news = NewsScraper(url, nthreads = 10)
    news.pull()
    news.scrape(number)
    texts = [article['text'] for article in news.polished()]
    print "Scraped %d articles" % len(texts)

    return texts

def get_topics_from_partitions(G, words_by_part, num_words_per_topic=10):
    topics = []
    for counter in xrange(0, len(words_by_part)):
        H = G.subgraph(words_by_part[counter])
        topics.append(graph_cluster.pagerank_top_k(H, num_words_per_topic).tolist())

    return topics

def print_topics_from_partitions(G, words_by_part, num_words_per_topic=10):

    for counter in xrange(0, len(words_by_part)):
        print '\nTopic {}:\n----------'.format(counter)
        H = G.subgraph(words_by_part[counter])
        print ', '.join(graph_cluster.pagerank_top_k(H, num_words_per_topic))

def get_topics_by_standard_words(num_news, draw=False, url='http://cnn.com'):

    texts = get_news(url, num_news)

    gb = SimpleGraphBuilder(text_processing.clean_punctuation_and_stopwords)
    gb.load_texts(texts)
    G = gb.create_graph()
    print "Graph built"

    partition = community.best_partition(G)
    words_by_part = get_words_by_partition(partition)

    print_topics_from_partitions(G, words_by_part, 10)
    if draw:
        values = [partition.get(node) for node in G.nodes()]
        nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
        plt.show()

    return G

def get_topics_non_dictionary(num_news, draw=False, url='http://cnn.com'):

    texts = get_news(url, num_news)

    gb = SimpleGraphBuilder(text_processing.only_non_dictionary_words, stem_words=False)
    gb.load_texts(texts)
    G = gb.create_graph()
    print "Graph built"

    partition = community.best_partition(G)
    words_by_part = get_words_by_partition(partition)

    mod = community.modularity(partition,G)
    print("modularity:", mod)

    print_topics_from_partitions(G, words_by_part, 10)
    if draw:
        values = [partition.get(node) for node in G.nodes()]
        nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
        plt.show()

    return G

def get_topics_noun_phrases(num_news, draw=False, url='http://cnn.com'):

    texts = get_news(url, num_news)

    gb = NounPhraseGraphBuilder(text_processing.clean_punctuation_and_stopwords)
    gb.load_texts(texts)
    G = gb.create_graph()
    print "Graph built"

    partition = community.best_partition(G)
    words_by_part = get_words_by_partition(partition)

    print_topics_from_partitions(G, words_by_part, 10)

    mod = community.modularity(partition,G)
    print("modularity:", mod)

    print_topics_from_partitions(G, words_by_part, 10)
    if draw:
        values = [partition.get(node) for node in G.nodes()]
        nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values, node_size=30, with_labels=False)
        plt.show()

    return G

def get_topics_non_dictionary_overlapping(num_news, k, url='http://cnn.com'):

    texts = get_news(url, num_news)

    gb = SimpleGraphBuilder(text_processing.only_non_dictionary_words, stem_words=False)
    gb.load_texts(texts)
    G = gb.create_graph()
    print "Graph built"

    words_by_part = graph_cluster.get_overlap_clusters(G, k, 1)

    print_topics_from_partitions(G, words_by_part, 10)

    return G

def get_topics_noun_phrases_overlapping(num_news, k, url='http://cnn.com'):

    texts = get_news(url, num_news)

    gb = NounPhraseGraphBuilder(text_processing.clean_punctuation_and_stopwords)
    gb.load_texts(texts)
    G = gb.create_graph()
    print "Graph built"

    words_by_part = graph_cluster.get_overlap_clusters(G, k, 1)

    print_topics_from_partitions(G, words_by_part, 10)

    return G
