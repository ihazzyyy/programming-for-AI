import nltk
from nltk.corpus import movie_reviews
import random
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy

nltk.download('movie_reviews')

documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:2000] 

def document_features(document):
    words = set(document)
    features = {}
    for word in word_features:
        features[f'contains({word})'] = (word in words)
    return features

featuresets = [(document_features(d), c) for (d, c) in documents]

train_set, test_set = featuresets[:1500], featuresets[1500:]

classifier = NaiveBayesClassifier.train(train_set)
print("Accuracy:", accuracy(classifier, test_set))


classifier.show_most_informative_features(10)

new_sentence = "I really hated the movie, it was awful!"
new_features = document_features(new_sentence.split())
print("Classification:", classifier.classify(new_features))
