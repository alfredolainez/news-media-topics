import numpy
import words_graph
import graph_cluster
import text_processing
import community
import topics
import codecs

def get_gold_topics(filename):
    FileIn = open(filename)
    LinesIn = FileIn.readlines()
    Topics = []
    for line in LinesIn:
        if line[0:5] == "TOPIC":
            continue
        Topics.append(line.strip().split(' '))
    return Topics

def read_golden_file(filename):
    text = ""
    file = codecs.open(filename, encoding='utf-8')
    for line in file:
        if line[0:6] == "TOPICS":
            break
        else:
            text += line

    return text

def get_texts():
    texts = []
    for i in range(1, 18):
        texts.append(read_golden_file("gold/" + str(i) + ".txt"))
    return texts

def evaluate():

    texts = get_texts()
    gb = words_graph.SimpleGraphBuilder(text_processing.clean_punctuation_and_stopwords, stem_words=False)
    #gb = words_graph.SimpleGraphBuilder(text_processing.only_non_dictionary_words, stem_words=False)
    #gb = words_graph.WindowGraphBuilder(text_processing.clean_punctuation_and_stopwords, stem_words=False)
    #gb = words_graph.NounPhraseGraphBuilder(text_processing.only_non_dictionary_words, stem_words=False)

    gb.load_texts(texts)
    G = gb.create_graph()

    partition = community.best_partition(G)
    #words_by_part = topics.get_words_by_partition(partition)
    words_by_part = graph_cluster.get_overlap_clusters(G, 9, 1)

    computed_topics = topics.get_topics_from_partitions(G, words_by_part)

    #Word splitter
    # computed_topics2 = []
    # for topic in computed_topics:
    #     new_topic = []
    #     for phrase in topic:
    #         new_topic.extend(phrase.split(' '))
    #     computed_topics2.append(new_topic)

    print compute_score(computed_topics, true_topics)

    #topics.print_topics_from_partitions(G, words_by_part, 10)


def compute_score(computed_topics, real_topics):

    topics_scores = []

    for topic in computed_topics:
        max_intersection = 0
        max_len = 0
        for test_topic in real_topics:
            common_words = len(list(set(topic) & set(test_topic)))
            if common_words > max_intersection:
                max_intersection = common_words
                max_len = len(test_topic)


        # Compute score for the topic
        score = 0
        if max_intersection > 0:
            score = 1
            score += ((max_intersection - 1) * 1.0/max((min(max_len, len(topic)) - 1), 1))**(1.0/3)

        topics_scores.append(score)

    return numpy.mean(topics_scores)/2

true_topics = get_gold_topics('gold/topics.txt')

if __name__ == '__main__':
    """ 
    debugging  code
    """
    print true_topics



#true_topics = [['typhoon', 'philippines', 'rain', 'storm', 'flooding', 'rainfall', 'winds', 'hagupit', 'tacloban', 'cyclone', 'assistance', 'manila'],
#          ['hostage', 'escape', 'philippines', 'islamist', 'extremists', 'swiss', 'rebels', 'shoot', 'military', 'injury'],
#          ['isis', 'iran', 'united', 'states', 'military', 'bombing', 'terrorist', 'islamist', 'secretary', 'obama', 'kobani', 'syria', 'civilians', 'warplanes', 'mortar', 'fight', 'graves', 'died'],
#          ['obama', 'president', 'throat', 'inflammation', 'sore', 'hospital', 'health', 'acid', 'white', 'physician'],
#          ['mars', 'nasa', 'science', 'fiction', 'space', 'human', 'earth', 'comet', 'technology', 'women', 'orion', 'capsule', 'first', 'flight', 'astronauts', 'craft', 'test'],
#          ['obama', 'racism', 'interview', 'progress', 'police', 'racial', 'tensions', 'black', 'death', 'race', 'eric', 'garner', 'daughter', 'officer', 'death', 'chokehold', 'jail', 'new york', 'justice', 'camera', 'cops', 'officers', 'body', 'video', 'law', 'death' ],
#          ['clinton', 'secretary', 'presidential', 'speech', 'gathering', 'obama'],
#          ['iran', 'correspondent', 'laws', 'charged', 'tehran', 'detained', 'american', 'arrest', 'crimes', 'imprisonment'],
#          ['clinton', 'obama', 'iran', 'nuclear', 'negotiation', 'presidential', 'communications', 'secretary', 'deal', 'israel' ],
#          ['israel', 'syria', 'strike', 'military', 'attack', 'war', 'warplanes', 'target', 'weapons', 'obama'],
#          ['qaeda', 'leaders', 'killed', 'attack', 'taliban', 'pakistan', 'afghanistan', 'border', 'bomb', 'military'],
#          ['obama', 'hostage', 'rescue', 'attempt', 'raid','killed', 'yemen', 'qaeda', 'forces', 'secretary']]

# computed_topics = [[u'shukrijumah',
#   u'qaeda',
#   u'al',
#   u'zazi',
#   u'pakistan',
#   u'florida',
#   u'new',
#   u'leaders',
#   u'afghanistan',
#   u'attacks'],
#  [u'said',
#   u'us',
#   u'somers',
#   u'official',
#   u'hostages',
#   u'korkie',
#   u'luke',
#   u'two',
#   u'rescue',
#   u'forces'],
#  [u'syria',
#   u'israeli',
#   u'syrian',
#   u'kobani',
#   u'near',
#   u'years',
#   u'old',
#   u'israel',
#   u'ali',
#   u'7'],
#  [u'police',
#   u'cameras',
#   u'cops',
#   u'also',
#   u'video',
#   u'body',
#   u'officers',
#   u'garner',
#   u'nt',
#   u'make'],
#  [u'nasa',
#   u'mars',
#   u'stofan',
#   u'orion',
#   u'earth',
#   u'astronauts',
#   u'space',
#   u'apollo',
#   u're',
#   u'science'],
#  [u'iran',
#   u'isis',
#   u'military',
#   u'states',
#   u'united',
#   u'iraq',
#   u'iranian',
#   u'islamic',
#   u'baghdad',
#   u'fars'],
#  [u'people',
#   u'typhoon',
#   u'storm',
#   u'hagupit',
#   u'sunday',
#   u'cnn',
#   u'tacloban',
#   u'one',
#   u'philippines',
#   u'many'],
#  [u'clinton',
#   u'women',
#   u'justice',
#   u'system',
#   u'stage',
#   u'balance',
#   u'administration',
#   u'talks',
#   u'audience',
#   u'america'],
#  [u'president',
#   u'obama',
#   u'throat',
#   u'ct',
#   u'scan',
#   u'white',
#   u'house',
#   u'acid',
#   u'medical',
#   u'doctor']]
#
# compute_score(computed_topics, true_topics)
