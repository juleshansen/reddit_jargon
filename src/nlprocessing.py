from nltk.corpus import stopwords, words
from nltk.stem import WordNetLemmatizer
import gensim
from collections import defaultdict
import contractions
import re
import string


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

    def __init__(self):
        '''
        Initialize object with an english dictionary and a list of stopwords.
        '''
        self.stopwords = set(stopwords.words('english'))
        self.eng_dict = set(words.words())

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
        strip_punc = re.compile('[%s0-9]' % re.escape(string.punctuation))
        no_punc = [strip_punc.sub('', comment.lower())
                   for comment in self.corpus]
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

    def __filter_english(self):
        return [
            [word for word in comment
                if word not in self.eng_dict]
            for comment in self.corpus
        ]

    def fit(self, corpus, frequency=0):
        '''
        Call to process corpus.

        Creates attributes:
        corpus - processed full set
        gensim_dictionary - a dictionary formatted for input into gensim
        gensim_dictionary_filtered - same as above, but removed words found
            in the provided english dictionary and terms that as many or fewer
            times than the frequency variable
        gensim_corpus - corpus formatted for gensim
        gensim_corpus_filtered - same as above, but removed words found
            in the provided english dictionary and terms that as many or fewer
            times than the frequency variable
        '''
        self.corpus = corpus
        self.corpus = self.__expand_contractions()
        self.corpus = self.__strip_punctuation()
        self.corpus = self.__lemmatize()
        self.__frequency_dict()
        self.gensim_dictionary = gensim.corpora.Dictionary(self.corpus)
        temp = self.gensim_dictionary[0]
        self.gensim_dictionary.filter_extremes(
            no_below=frequency,
            no_above=1.0)
        del temp
        self.gensim_corpus = [
            self.gensim_dictionary.doc2bow(text) for text in self.corpus
            ]
        # Apply filtering from here on
        self.apply_filter(frequency)

    def return_frequency_filter(self, frequency=1):
        freq_filter = [
            [token for token in text if self.frequency_dict[token] > frequency]
            for text in self.corpus
        ]
        return freq_filter

    def apply_filter(self, frequency=1):
#         self.corpus_filtered = self.return_frequency_filter(frequency)
        self.corpus_filtered = self.__filter_english()
#         self.gensim_dictionary_filtered = gensim.corpora.Dictionary(
#             self.corpus)
#         temp = self.gensim_dictionary_filtered[0]
#         del temp
        self.gensim_corpus_filtered = [
            self.gensim_dictionary.doc2bow(text)
            for text in self.corpus_filtered
            ]
