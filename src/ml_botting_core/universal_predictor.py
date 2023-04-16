if 'logger' in locals() or 'logger' in globals():
    from loguru import logger

class universal_predictor:
    def __new__(cls):  # make singleton
        if not hasattr(cls, 'instance'):
            cls.instance = super(universal_predictor, cls).__new__(cls)
            cls.instance.__initialized = False
        else:
            logger.debug('universal_predictor returning existing')
        return cls.instance

    def __init__(self, logger):
        if (self.__initialized): return  # make singleton
        self.__initialized = True
        logger.debug('universal_predictor initialized')
        self.classifiers = {}
        self.regressors = {}

    def load_models(self):
        return ''
