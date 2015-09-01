from __future__ import division
from marmot.features.feature_extractor import FeatureExtractor
import logging
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger('testlogger')


class TokenCountFeatureExtractor(FeatureExtractor):

    def get_features(self, context_obj):
        target_len = len(context_obj['token'])
        target_tok_len = np.average([len(context_obj['token'])])
        source_len, source_tok_len = 0, 0
        if 'source_token' in context_obj:
            source_len = len(context_obj['source_token'])
            source_tok_len = np.average([len(context_obj['source_token'])])

        return [target_len, source_len, source_len/target_len, target_tok_len, source_tok_len]

    def get_feature_names(self):
        return ['target_phrase_len', 'source_phrase_len', 'source_target_len_ratio', 'avg_target_token_len', 'avg_source_token_len']
