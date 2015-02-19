from nltk import ngrams, word_tokenize
import codecs

from marmot.features.feature_extractor import FeatureExtractor
from marmot.util.ngram_window_extractor import extract_window, left_context, right_context


# Class that extracts various LM features
# Calling an external LM is very slow, so a new lm is constructed with nltk
class LMFeatureExtractor(FeatureExtractor):

    def __init__(self, corpus_file, order=3):

        self.order = order
        self.lm = [set() for i in range(order)]
        for line in codecs.open(corpus_file, encoding='utf-8'):
            words = [u'_START_'] + word_tokenize(line[:-1]) + [u'_END_']
            for i in range(1, order):
                self.lm[i] = self.lm[i].union(ngrams(words, i+1))
            self.lm[0] = self.lm[0].union(words)

    def check_lm(self, ngram, side='left'):
        for i in range(self.order, 0, -1):
            if side == 'left':
                cur_ngram = ngram[len(ngram)-i:]
            elif side == 'right':
                cur_ngram = ngram[:i]
            if tuple(cur_ngram) in self.lm[i-1]:
                return i
        return 0

    def get_backoff(self, ngram):
        assert(len(ngram) == 3)
        ngram = tuple(ngram)
        if ngram in self.lm[2]:
            return 1.0
        elif ngram[:2] in self.lm[1] and ngram[1:] in self.lm[1]:
            return 0.8
        elif ngram[1:] in self.lm[1]:
            return 0.6
        elif ngram[:2] in self.lm[1] and ngram[2] in self.lm[0]:
            return 0.4
        elif ngram[1] in self.lm[0] and ngram[2] in self.lm[0]:
            return 0.3
        elif ngram[2] in self.lm[0]:
            return 0.2
        else:
            return 0.1

    # returns a set of features related to LM
    # currently extracting: highest order ngram including the word and its LEFT context,
    #                       highest order ngram including the word and its RIGHT context
    def get_features(self, context_obj):
        idx = context_obj['index']

        left_ngram = left_context(context_obj['target'], context_obj['token'], context_size=self.order-1, idx=idx) + [context_obj['token']]
        right_ngram = [context_obj['token']] + right_context(context_obj['target'], context_obj['token'], context_size=self.order-1, idx=idx)
        left_ngram_order = self.check_lm(left_ngram, side='left')
        right_ngram_order = self.check_lm(right_ngram, side='right')

        left_trigram = left_context(context_obj['target'], context_obj['token'], context_size=2, idx=idx) + [context_obj['token']]
        middle_trigram = extract_window(context_obj['target'], context_obj['token'], idx=idx)
        right_trigram = [context_obj['token']] + right_context(context_obj['target'], context_obj['token'], context_size=2, idx=idx)

        backoff_left = self.get_backoff(left_trigram)
        backoff_middle = self.get_backoff(middle_trigram)
        backoff_right = self.get_backoff(right_trigram)

        return [left_ngram_order, right_ngram_order, backoff_left, backoff_middle, backoff_right]

    def get_feature_names(self):
        return ['highest_order_ngram_left', 'highest_order_ngram_right', 'backoff_behavior_left', 'backoff_behavior_middle', 'backoff_behavior_right']