import itertools
import networkx as nx
import nltk
from nltk.stem.porter import PorterStemmer
import igraph
from tagger import GetNounPhrases

def stem_words(tokens, language='english'):
    """
    Stems words in a list of tokens
    """
    stemmer = PorterStemmer()
    stemmed_words = []
    for token in tokens:
        stemmed_words.append(stemmer.stem(token))

    return stemmed_words

class GraphBuilder(object):
    """
    Generic class for graph builders. It serves as a base class with a basic framework
    for text capabilities for building graphs.
    Class parameters:
        text_cleaner: function to apply to remove unimportant tokens
    Attributes:
        self.texts: raw unicode texts loaded
        self.text_sentences: for each text, list of tokenized and cleaned sentences
    """
    def __init__(self, text_cleaner=None, stem_words=True):
        self.text_cleaner = text_cleaner
        self.stem_words = stem_words
        self.texts = []
        self.text_sentences = []

    def sentence_extractor(self):
        """
        Extracts sentences from the loaded texts in the object
        """
        self.text_sentences = []
        for text in self.texts:
            sentences = nltk.sent_tokenize(text)
            tokens_sentences = []
            for sentence in sentences:
                tokens = nltk.word_tokenize(sentence)
                if self.text_cleaner is not None:
                    tokens = self.text_cleaner(tokens)
                    if self.stem_words:
                        tokens = stem_words(tokens)
                    
                tokens_sentences.append(tokens)
            self.text_sentences.append(tokens_sentences)

    def load_texts(self, texts):
        """
        Texts must be a list of unicode strings
        """
        # Initial treatment of texts. Everything is lowered
        self.texts = []
        for text in texts:
            self.texts.append(text.lower())

        self.sentence_extractor()


class SimpleGraphBuilder(GraphBuilder):
    """
    SimpleGraphBuilder. It builds an undirected graph with two words connected
    by an edge with weight the number of times they appear in the same document
    """

    def __init__(self, text_cleaner=None, stem_words=True):
        super(SimpleGraphBuilder, self).__init__(text_cleaner, stem_words)
        self.text_cleaner = text_cleaner

    def create_graph(self):
        G=nx.Graph() 
        for text in self.text_sentences:
            text_words = []
            for sentence in text:
                G.add_nodes_from(sentence)
                text_words += sentence
            for (a,b) in itertools.combinations(text_words,2):
                if G.has_edge(a,b):
                    G[a][b]['weight'] = G.get_edge_data(a,b)['weight'] + 1
                else:
                    G.add_edge(a,b, weight=1. )
        return G

    def create_igraph(self):
        G = igraph.Graph()
        G.es['weight'] = 1.0
        first_node = True
        for text in self.text_sentences:
            print "A text"
            text_words = []
            for sentence in text:
                print "A sentence"
                for token in sentence:
                    ## if not 'name' in G.vs: Try to find way!
                    if first_node:
                        G.add_vertex(name=token)
                        first_node = False
                    elif token not in G.vs['name']:
                        G.add_vertex(name=token)
                text_words += sentence
            for (a,b) in itertools.combinations(text_words, 2):
                if a != b:
                    if G[a,b] != 0:
                        G[a,b] = G[a,b] + 1
                    else:
                        G[a,b] = 1
        return G

    # Improved version: using nodes by ids and keeping the difference ourselves
    def create_igraph2(self):
        ids_by_token = {}
        current_id = 0
        G = igraph.Graph()
        G.es['weight'] = 1.0

        n_text = 1

        for text in self.text_sentences:
            print "Processing text %d of %d" % (n_text, len(self.text_sentences))
            text_words = []
            for sentence in text:
                for token in sentence:
                    if not token in ids_by_token:
                        G.add_vertex(name=token)
                        ids_by_token[token] = current_id
                        current_id += 1
                text_words += sentence
            for (token_a,token_b) in itertools.combinations(text_words, 2):
                a = ids_by_token[token_a]
                b = ids_by_token[token_b]
                if a != b:
                    if G[a,b] != 0:
                        G[a,b] = G[a,b] + 1
                    else:
                        G[a,b] = 1
            n_text += 1
        return G, ids_by_token

def n_word_window(sentence, n = 2):
    tuples = []
    for i in xrange(0, (len(sentence) - n + 1)):
        for w in xrange(1, n):
            tuples.append((sentence[i], sentence[i + w]))
    return tuples

class WindowGraphBuilder(GraphBuilder):
    """
    Makes a graph with a n-word moving window. Example:
    This is a sentence. This is another sentence a kid could write.
    \____/                              \________/
      a                                  same as b
    \_______/                           \____________/
        b                                      d
    \_________________/                 \_________________/
             c                                    e
    """
    def __init__(self, text_cleaner=None, stem_words=True):
        super(WindowGraphBuilder, self).__init__(text_cleaner, stem_words)
        self.text_cleaner = text_cleaner

    def create_graph(self, n = 2):

        G = nx.Graph() 

        for text in self.text_sentences:
            text_words = []
            for sentence in text:
                if not(len(sentence) == 1):
                    G.add_nodes_from(sentence)
                    text_words += sentence
            for sentence in text:
                if not (len(sentence) == 1):
                    for (a, b) in n_word_window(sentence, n):
                        if G.has_edge(a, b):
                            G[a][b]['weight'] = G.get_edge_data(a,b)['weight'] + 1.0
                        else:
                            G.add_edge(a, b, weight=1.)
        return nx.connected_component_subgraphs(G).next()



class NounPhraseGraphBuilder(GraphBuilder):
    '''
    Tags noun phrases, makes them the nodes. 
    You can choose what type of graph to 
    construct with the create_graph() function.
    '''
    def __init__(self, text_cleaner=None, stem_words=False):
        super(NounPhraseGraphBuilder, self).__init__(text_cleaner, stem_words)
        self.text_cleaner = text_cleaner

    def sentence_extractor(self):
        """
        Extracts sentences from the loaded texts in the object
        """
        self.text_sentences = []
        for text in self.texts:
            sentences = nltk.sent_tokenize(text)
            tokens_sentences = []
            for sentence in sentences:
                # tokens = nltk.word_tokenize(sentence)
                tokens = GetNounPhrases(sentence)
                if self.text_cleaner is not None:
                    tokens = self.text_cleaner(tokens)
                    if self.stem_words:
                        tokens = stem_words(tokens)
                    
                tokens_sentences.append(tokens)
            self.text_sentences.append(tokens_sentences)

    def create_graph(self, graphtype = 'occurence', n = 2):

        G = nx.Graph() 
        if graphtype.lower() == 'ngram':
            for text in self.text_sentences:
                text_words = []
                for sentence in text:
                    if not(len(sentence) == 1):
                        G.add_nodes_from(sentence)
                        text_words += sentence
                for sentence in text:
                    if not (len(sentence) == 1):
                        for (a, b) in n_word_window(sentence, n):
                            if G.has_edge(a, b):
                                G[a][b]['weight'] = G.get_edge_data(a,b)['weight'] + 1.0
                            else:
                                G.add_edge(a, b, weight=1.)
            return nx.connected_component_subgraphs(G).next()
        elif graphtype.lower() == 'occurence':
            for text in self.text_sentences:
                text_words = []
                for sentence in text:
                    G.add_nodes_from(sentence)
                    text_words += sentence
                for (a,b) in itertools.combinations(text_words,2):
                    if G.has_edge(a,b):
                        G[a][b]['weight'] = G.get_edge_data(a,b)['weight'] + 1
                    else:
                        G.add_edge(a,b, weight=1. )
            return G
        else:
            raise ValueError, 'graphtype can be either \'occurence\', or \'ngram\'.'
    

        









