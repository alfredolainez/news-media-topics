
from words_graph import SimpleGraphBuilder, NounPhraseGraphBuilder
from extractor import NewsScraper
import graph_cluster
import text_processing
import time
import community


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
    news = NewsScraper('http://cnn.com', nthreads = 10)
    news.pull()
    news.scrape(20)
    texts = (article['text'] for article in news.polished())

    return texts

def print_topics_from_partitions(G, words_by_part, num_words_per_topic=10):

    for counter in xrange(0, len(words_by_part)):
        print '\nTopic {}:\n----------'.format(counter)
        H = G.subgraph(words_by_part[counter])
        print ', '.join(graph_cluster.pagerank_top_k(H, num_words_per_topic))

def get_topics_by_standard_words(num_news, url='http://cnn.com'):

    texts = get_news(url, num_news)

    gb = SimpleGraphBuilder(text_processing.clean_punctuation_and_stopwords)
    gb.load_texts(texts)
    G = gb.create_graph()
    print "Graph built"

    partition = community.best_partition(G)
    words_by_part = get_words_by_partition(partition)

    print_topics_from_partitions(G, words_by_part, 10)

    return G

def get_topics_non_dictionary(num_news, url='http://cnn.com'):

    texts = get_news(url, num_news)

    gb = SimpleGraphBuilder(text_processing.only_non_dictionary_words, stem_words=False)
    gb.load_texts(texts)
    G = gb.create_graph()
    print "Graph built"

    partition = community.best_partition(G)
    words_by_part = get_words_by_partition(partition)

    print_topics_from_partitions(G, words_by_part, 10)

    return G