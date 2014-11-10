import networkx as network
import nltk

class GraphBuilder:
    """
    Generic class for graph builders. It serves as a base class with a basic framework
    for text capabilities for building graphs.
    Class parameters:
        text_cleaner: function to apply to remove unimportant tokens
    Attributes:
        self.texts: raw unicode texts loaded
        self.text_sentences: for each text, list of tokenized and cleaned sentences
    """
    def __init__(self, text_cleaner=None):
        self.text_cleaner = text_cleaner
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

    def __init__(self, text_cleaner=None):
        self.text_cleaner = text_cleaner

    def create_graph(self):
        # TODO: Build graph
        pass


