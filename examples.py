from words_graph import SimpleGraphBuilder
from extractor import NewsScraper
import text_processing

news = NewsScraper('http://cnn.com', nthreads = 20)
news.pull()
news.scrape(10)
texts = (article['text'] for article in news.polished())

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

# Next steps: Build graph!!!
gb.create_graph()



