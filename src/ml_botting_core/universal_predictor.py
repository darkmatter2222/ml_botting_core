class universal_predictor:
    def __new__(cls, **args):  # make singleton
        if not hasattr(cls, 'instance'):
            cls.instance = super(universal_predictor, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance

    # logger available for dependency injection, no documentation why this is inappropriate.
    def __init__(self, config=None, logger=None, verbose=0):
        if (self.__initialized): return  # make singleton
        self.__initialized = True
        self.verbose = verbose
        self.logger = logger

        # region ----- validation
        if config is None:
            error = "universal_predictor missing configuration"
            self.log_error(error)
            raise Exception(error)
        # endregion

        self.classifiers = {}
        self.regressors = {}
        self.log_debug('universal_predictor initialized')

    # region ----- logging
    def log_debug(self, statement):
        if self.logger is not None and self.verbose >= 0:
            self.logger.debug(statement)

    def log_info(self, statement):
        if self.logger is not None and self.verbose >= 1:
            self.logger.info(statement)

    def log_warning(self, statement):
        if self.logger is not None and self.verbose >= 2:
            self.logger.warning(statement)

    def log_error(self, statement):
        if self.logger is not None and self.verbose >= 3:
            self.logger.error(statement)
    # endregion

    # region ----- load

