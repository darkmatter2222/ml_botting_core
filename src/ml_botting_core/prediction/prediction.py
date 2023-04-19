from PIL import Image
import numpy as np
import tensorflow as tf
import uuid


def predict(original_image, classifier, model_name):
    img = original_image.resize(
        (classifier['meta']['image_resize'][1],
         classifier['meta']['image_resize'][0]),
        resample=Image.Resampling.NEAREST)

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    id = uuid.uuid1()
    # TODO, Get back to this
    # if self.classifiers[model_name]['save_images']:
    # img.save(f"{self.config['log_dir']}\\{model_name}\\{id}.png")

    predictions = classifier['model'].predict(img_array)
    scores = tf.nn.softmax(predictions[0])
    result = {
        'argmax_index': np.argmax(scores),
        'value_at_argmax': scores[np.argmax(scores)].numpy(),
        'class': classifier['meta']['classes'][np.argmax(scores)],
        'classes': classifier['meta']['classes'],
        'scores': scores.numpy().tolist(),
        'id': id,
        'image_saved': 0,
        'model_name': model_name
    }

    return result
