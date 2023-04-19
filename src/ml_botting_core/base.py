from loguru import logger


from .model_management.model_manager import load_models_from_config
from .prediction import prediction


class universal_predictor:
    def __new__(cls, **args):  # make singleton
        if not hasattr(cls, 'instance'):
            cls.instance = super(universal_predictor, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance

    # logger available for dependency injection, no documentation why this is inappropriate.
    def __init__(self, config=None, verbose=0):
        if (self.__initialized): return  # make singleton
        self.__initialized = True
        self.verbose = verbose
        self.config = config
        self.classifiers = {}

        # region ----- validation
        if self.config is None:
            error = "universal_predictor missing configuration"
            logger.error(error)
            raise Exception(error)
        # endregion

        self.classifiers = {}
        self.regressors = {}
        logger.debug('universal_predictor initialized')

    # region ----- load
    def load_models(self):
        self.classifiers = load_models_from_config(self.config)
        return None

    # endregion

    # region ----- prediction
    def predict(self, original_image, model_name):
        result = prediction.predict(original_image, self.classifiers[model_name], model_name)
        return result
    # endregion
