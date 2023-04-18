import uuid
import sys

import tensorflow as tf
from loguru import logger
from PIL import Image
import numpy as np

sys.modules['ml_botting_core'] = sys.modules['src.ml_botting_core']

from ml_botting_core.model_management.model_manager import load_models_from_config


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

    # region ----- predict
    def predict(self, original_image, model_name):
        img = original_image.resize(
            (self.classifiers[model_name]['meta']['image_resize'][1],
             self.classifiers[model_name]['meta']['image_resize'][0]),
            resample=Image.Resampling.NEAREST)

        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch

        id = uuid.uuid1()
        # TODO, Get back to this
        #if self.classifiers[model_name]['save_images']:
            #img.save(f"{self.config['log_dir']}\\{model_name}\\{id}.png")

        predictions = self.classifiers[model_name]['model'].predict(img_array)
        scores = tf.nn.softmax(predictions[0])
        result = {
            'argmax_index': np.argmax(scores),
            'value_at_argmax': scores[np.argmax(scores)].numpy(),
            'class': self.classifiers[model_name]['meta']['classes'][np.argmax(scores)],
            'classes': self.classifiers[model_name]['meta']['classes'],
            'scores': scores.numpy().tolist(),
            'id': id,
            'image_saved': 0,
            'model_name': model_name
        }

        return result
    # endregion
