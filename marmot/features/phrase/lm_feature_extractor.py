import kenlm
from marmot.features.feature_extractor import FeatureExtractor


class LMFeatureExtractor(FeatureExtractor):

    def __init__(self, lm_file):
        self.model = kenlm.LanguageModel(lm_file)

    def get_features(self, context_obj):
        return self.model.score(' '.join(context_obj['token']))

    def get_feature_names(self):
        return ['target_log_prob']
