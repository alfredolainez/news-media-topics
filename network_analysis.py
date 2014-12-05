from words_graph import *
from text_processing import *
import networkx as nx
import matplotlib.pyplot as plt
from topics import *

#gb = SimpleGraphBuilder(text_cleaner=only_non_dictionary_words, stem_words=False)
#gb.load_texts([u"I went went there", u"Yes I was. Although I'd didn't see Obama!"])

def draw_example():
    article1 = u"Obama met yesterday in New York City with the UK prime minister Cameron in order to talk about the conflict in Israel. They discussed the implication of the USA and UK in the conflict and proper steps to peace"
    article2 = u"Israel's prime Minister Netanyahu replied today in Jerusalen to comments by US president Barack Obama. We do not need foreign implication in the conflict, he was reported to say"
    article3 = u"President Barack Obama was with King Philip I from Spain the last day in New York city. They talked about educational exchange programs."

    #gb = SimpleGraphBuilder(only_non_dictionary_words, stem_words=False)
    #gb = SimpleGraphBuilder(clean_punctuation_and_stopwords)
    gb = NounPhraseGraphBuilder(clean_punctuation_and_stopwords)
    gb.load_texts([article1, article2, article3])
    G = gb.create_graph()

    #nx.draw_networkx(G, node_size=500, with_labels=True, node_color='w', alpha=0.4, edge_color='m',
                     #font_size=11)
    nx.draw_networkx(G, node_size=300, with_labels=True, node_color='w', alpha=0.4, edge_color='m',
                     font_size=11)
    plt.axis('off')
    plt.show()

def draw_big_network():
    G = get_topics_non_dictionary(30)

    nx.draw_networkx(G, node_size=10, with_labels=False, node_color='w', alpha=0.4, edge_color='m',
                     font_size=11)
    plt.axis('off')
    plt.show()

    return G

def get_graph_stats(G):
    ccs = nx.connected_component_subgraphs(G)
    number_ccs = nx.number_connected_components(G)

    avg_shortest_path = 0.0 #nx.average_shortest_path_length(G)
    for g in ccs:
        avg_shortest_path += nx.average_shortest_path_length(g)
    avg_shortest_path /= number_ccs

    print nx.info(G)
    print "Connected components: " + str(number_ccs)
    print "Average shortest path: " + str(avg_shortest_path)

def plot_degree_distribution(G):

    degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
    #print "Degree sequence", degree_sequence
    dmax=max(degree_sequence)

    plt.loglog(degree_sequence,'b-')
    plt.ylabel("Degree")
    plt.xlabel("Rank")

    # draw graph in inset
    plt.axes([0.1,0.1,0.45,0.45])
    Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
    pos=nx.spring_layout(Gcc)
    plt.axis('off')
    nx.draw_networkx_nodes(Gcc,pos,node_size=20)
    nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

    plt.savefig("degree_histogram.png")
    plt.show()

