from words_graph import SimpleGraphBuilder
from extractor import NewsScraper
import graph_cluster
import text_processing
import time

t0 = time.time()

news = NewsScraper('http://cnn.com', nthreads = 20)
news.pull()
news.scrape(10)
texts = (article['text'] for article in news.polished())

t1 = time.time()
print "Data retrieved in %.2f sec" %(t1-t0)

# Create a graph builder
gb = SimpleGraphBuilder(text_processing.clean_punctuation_and_stopwords)

gb.load_texts(texts)

# Show texts in the builder
for text in texts:
    print text
    print "##################################################"

print "##################################################"
print  "TOKENIZED SENTENCES"
print "##################################################"

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
ex = 2
r = 2
tol = 1e-3
M = graph_cluster.MCL_cluster(G,ex,r,tol)
t3 = time.time()
print "Graph clustered in %.2f sec" %(t3-t2)