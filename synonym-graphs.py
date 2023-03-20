from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import nltk
import string
import networkx as nx
import community
from community import community_louvain
from collections import Counter
import sys

graph = nx.Graph()
direct_synonym = 1
indirect_synonym = .5


def get_wordnet_pos(word):
    tag = pos_tag([word])[0][1][0].upper()
    tag_map = {"J": wordnet.ADJ, "N": wordnet.NOUN,
               "V": wordnet.VERB, "R": wordnet.ADV}
    return tag_map.get(tag, wordnet.NOUN)


def text_processing(filename):
    file = open(filename, "r", encoding="utf-8")
    text = file.read()
    file.close()

    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens]
    punctuation_table = str.maketrans('', '', string.punctuation)
    stripped_tokens = [word.translate(punctuation_table) for word in tokens]

    words = [word for word in stripped_tokens if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if not word in stop_words]

    lemmatizer = WordNetLemmatizer()

    lemmas = [lemmatizer.lemmatize(
        word, get_wordnet_pos(word)) for word in words]
    lemmas = [word for word in lemmas if len(word) > 2]

    return lemmas


def word_count(lemmas):
    word_list = []

    for word in set(lemmas):
        count = lemmas.count(word)
        word_list.append((word, count))

    word_dict = dict(word_list)

    return word_dict


def return_synonyms(word):
    synonyms = []

    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    return (set(synonyms))


def create_graph(words, counts):
    parts_of_speech = {'JJ', 'JJR', 'JJS', 'NN',
                       'NNS', 'NNP', 'NNPS', 'RB', 'RBR', 'RBS'}

    for word in words:
        tagged_word = nltk.pos_tag([word])
        if tagged_word[0][1] in parts_of_speech:
            graph.add_node(word)
            graph.nodes[word]['word_frequency'] = counts[word]

    for node1 in graph:
        synonyms_set = return_synonyms(node1)
        for node2 in graph:
            if node2 in synonyms_set:
                if node1 != node2:
                    graph.add_edge(node1, node2)
                    graph[node1][node2]['weight'] = direct_synonym

    print("Graph created (synonyms level 1)")
    print(f"Verties = {graph.number_of_nodes()}")
    print(f"Edges = {graph.number_of_edges()}")


def expand_graph():

    for u in list(graph.nodes()):
        for v in list(graph.nodes()):
            if u != v and v not in graph.neighbors(u):
                synset1 = return_synonyms(u)
                synset2 = return_synonyms(v)
                common_word = any(item in synset1 for item in synset2)
                if common_word is True:
                    graph.add_edge(u, v)
                    graph[u][v]['weight'] = indirect_synonym

    print("Graph created (synonyms level 1)")
    print(f"Verties = {graph.number_of_nodes()}")
    print(f"Edges = {graph.number_of_edges()}")


def clean_graph():

    count = 0
    for u in list(graph.nodes()):
        if graph.degree[u] == 0 and graph.nodes[u]['word_frequency'] == 1:
            graph.remove_node(u)
            count += 1

    print(f"{count} words have been removed")
    print("Graph (synonyms level 2) - after cleaning:")
    print(f"Verties = {graph.number_of_nodes()}")
    print(f"Edges = {graph.number_of_edges()}")


def find_communities():
    parts = community_louvain.best_partition(graph)
    nx.set_node_attributes(graph, parts, 'community_number')
    size = len(set(parts.values()))
    print(f"\n Number of communities =  {size}\n")
    modularity = community.modularity(parts, graph)
    print(f"\n Modularity = {modularity}\n")
    return parts


def generate_word(words):
    synonyms = []
    for word in words:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.name() != word:
                    synonyms.append(lemma.name())

    synonyms_counts = Counter(synonyms)
    representative_word = synonyms_counts.most_common(1)[0][0]
    return representative_word


def analyze_communities(partition, number_of_key_words):

    print("\n\n")
    count = 0
    for community in set(partition.values()):
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == community]
        if len(list_nodes) > 1:
            subgraph = graph.subgraph(list_nodes)
            if nx.average_clustering(subgraph) != 0.0:
                print(f"Community {subgraph.nodes()}")
                print(f"Number of Vertices = ", len(subgraph))
                print(f"Number of Edges = ", subgraph.number_of_edges())
                print(f"Diameter = ", nx.diameter(subgraph))
                print(f"Avg Clustering Coefficient = ",
                      nx.average_clustering(subgraph))
                s = 0
                for u in list(subgraph.nodes()):
                    s = s + subgraph.nodes[u]['word_frequency']
                print("Community weight = ", s)

                degree = nx.degree_centrality(subgraph)
                sorted_ = {k: v for k, v in sorted(
                    degree.items(), key=lambda item: item[1], reverse=True)}
                key_words = list(sorted_)[:number_of_key_words]

                community_name = generate_word(key_words)
                print(f"Community Name = {community_name}")

            #    bet = nx.betweenness_centrality(subgraph)
            #    sorted_ = {k: v for k, v in sorted(
            #        bet.items(), key=lambda item: item[1], reverse=True)}
            #    print("******\nSorted betweenness cent nodes:")
            #    key_words = list(sorted_)[:number_of_key_words]
            #    print(key_words)

            #    clos = nx.closeness_centrality(subgraph)
            #    sorted_ = {k: v for k, v in sorted(
            #        clos.items(), key=lambda item: item[1], reverse=True)}
            #    print("******\nSorted closeness cent nodes:")
            #    key_words = list(sorted_)[:number_of_key_words]
            #    print(key_words)

                print("--------------------------------------------")


def main():
    filename = sys.argv[1]
    number_of_key_words = int(sys.argv[2])

    lemmas = text_processing(filename)
    word_dict = word_count(lemmas)
    create_graph(lemmas, word_dict)
    expand_graph()
    clean_graph()
    partition = find_communities()
    analyze_communities(partition, number_of_key_words)

    print("Done!")


if __name__ == "__main__":
    main()
