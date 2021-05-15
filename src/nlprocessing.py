from nltk.corpus import stopwords, words
from nltk.stem import WordNetLemmatizer
import gensim
from collections import defaultdict
import contractions
import re
import string

eng_dict = set(words.words())
stops = set(stopwords.words('english'))


class ProcessCorpus():
    '''
    Class for NLP processign to create a corpus that has:
      - contractions expanded
      - punctuation stripped
      - lemmatizaion
    There is an optional frequency filter included to remove words that appear
    less than some number of times.

    This class has stored attributes for a dictionary and corpus object to be
    supplied to gensim.
    '''

    def __init__(self, stopwords=stops, eng_dict=eng_dict):
        self.stopwords = stopwords
        self.eng_dict = eng_dict

    def __expand_contractions(self):
        '''
        Expands contraction words such as don't --> do not prior to removing
        punctuation so meaning isn't lost and words will still appear in
        supplied dictionary for dictionary filtering.
        '''
        expanded = [
            contractions.fix(comment.lower()) for comment in self.corpus
            ]
        return expanded

    def __strip_punctuation(self):
        '''
        Removes all punctuation from corpus.
        '''
        strip_punc = re.compile('[%s]' % re.escape(string.punctuation))
        no_punc = [strip_punc.sub('', comment) for comment in self.corpus]
        return no_punc

    def __lemmatize(self):
        '''
        Lemmatizes words using NLTK package's WordNetLemmatizer.
        '''
        split = []
        lemma = WordNetLemmatizer()
        for comment in self.corpus:
            split.append(
                [lemma.lemmatize(word) for word in comment.split()
                    if word not in self.stopwords]
                )
        return split

    def __frequency_dict(self):
        '''
        Creates a dictionary of word frequencies in the corpus to be used for
        frequency filtering. Good for removing typos, and words that are not
        frequent enough to be considered slang due to low adoption by
        subculture.
        '''
        self.frequency_dict = defaultdict(int)
        for text in self.corpus:
            for token in text:
                self.frequency_dict[token] += 1

    def fit(self, corpus):
        '''
        Call to process corpus.

        Creates attributes:
        corpus - processed
        gensim_dictionary
        '''
        self.corpus = corpus
        self.corpus = self.__expand_contractions()
        self.corpus = self.__strip_punctuation()
        self.corpus = self.__lemmatize()
        self.__frequency_dict()
        self.gensim_dictionary = gensim.corpora.Dictionary(self.corpus)
        temp = self.gensim_dictionary[0]
        del temp
        self.gensim_corpus = [
            self.gensim_dictionary.doc2bow(text) for text in self.corpus
            ]

    def return_frequency_filter(self, frequency=1):
        freq_filter = [
            [token for token in text if self.frequency_dict[token] > frequency]
            for text in self.corpus
        ]
        return freq_filter

    def apply_frequency_filter(self, frequency=1):
        self.corpus_freq = self.return_frequency_filter(frequency)
        self.gensim_dictionary_freq = gensim.corpora.Dictionary(self.corpus)
        temp = self.gensim_dictionary_freq
        del temp
        self.gensim_corpus_freq = [
            self.gensim_dictionary.doc2bow(text) for text in self.corpus
            ]
