from sklearn.base import TransformerMixin


__author__ = 'Elisha Yadgaran'


class BaseTransformer(TransformerMixin):
    '''
    Base Transformer class that implements all the necessary methods

    Default behavior is to do nothing - overwrite later
    '''
    def fit(self, X, y=None, **kwargs):
        return self

    def transform(self, X, y=None, **kwargs):
        return X

    def get_params(self, **kwargs):
        '''
        Should only return seeding parameters, not fit ones
        (ie params of unfit object should be identical to fit object)
        '''
        return {}

    def set_params(self, **kwargs):
        pass

    def get_feature_names(self, input_feature_names):
        return input_feature_names
