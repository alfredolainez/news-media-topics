from words_graph import SimpleGraphBuilder
import text_processing

text1 = u"The DiGraph class provides additional methods specific to directed edges, e.g. DiGraph.out_edges(), DiGraph.in_degree(), DiGraph.predecessors(), DiGraph.successors() etc. To allow algorithms to work with both classes easily, the directed versions of neighbors() and degree() are equivalent to successors() and the sum of in_degree() and out_degree() respectively even though that may feel inconsistent at times."
text2 = u"NetworkX provides classes for graphs which allow multiple edges between any pair of nodes. The MultiGraph and MultiDiGraph classes allow you to add the same edge twice, possibly with different edge data. This can be powerful for some applications, but many algorithms are not well defined on such graphs. Shortest path is one example. Where results are well defined, e.g. MultiGraph.degree() we provide the function. Otherwise you should convert to a standard graph in a way that makes the measurement well defined."
texts = [text1, text2]


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
for text in gb.text_sentences:
    print "##################################################"
    for sentence in text:
        print sentence

# Next steps: Build graph!!!
gb.create_graph()



