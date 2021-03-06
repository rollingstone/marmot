import kenlm
from marmot.features.feature_extractor import FeatureExtractor


class SourceLMFeatureExtractor(FeatureExtractor):

    def __init__(self, lm_file):
        self.model = kenlm.LanguageModel(lm_file)

    def get_features(self, context_obj):
        if 'source_token' in context_obj and len(context_obj['source_token']) > 0:
            log_prob = self.model.score(' '.join(context_obj['source_token']), bos=False, eos=False)
            src_len = len(context_obj['source_token'])
            perplexity = 2**((-1/src_len)*log_prob)
            return [log_prob, perplexity]
        else:
            return [0.0, 0.0]

    def get_feature_names(self):
        return ['source_log_prob', 'source_perplexity']
