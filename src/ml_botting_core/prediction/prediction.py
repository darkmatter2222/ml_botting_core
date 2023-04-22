from PIL import Image
import numpy as np
import tensorflow as tf
import uuid
import json
import datetime
import os
import time


def write_json(new_data, filename):
    if not os.path.isfile(filename):
        file = open(filename, 'w+')
        file.write(json.dumps({"results": []}, indent=1))
        file.close()
        time.sleep(0.1)

    file = open(filename, 'r')
    content = file.read()
    file.close()

    file_data = json.loads(content)
    file_data['results'].append(new_data)

    file = open(filename, 'w')
    file.write(json.dumps(file_data, indent=1))
    file.close()


def save_image(id, original_image, classifier, model_name, result):
    if bool(classifier['config_record']['save_images']):
        original_image.save(f"{classifier['config_record']['model_log_directory']}\\{id}.png")
        write_json(result, f"{classifier['config_record']['model_log_directory']}\\image_data.json")


def predict(original_image, classifier, model_name):
    img = original_image.resize(
        (classifier['meta']['image_resize'][1],
         classifier['meta']['image_resize'][0]),
        resample=Image.Resampling.NEAREST)

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    id = str(uuid.uuid1())
    predictions = classifier['model'].predict(img_array)
    scores = tf.nn.softmax(predictions[0])
    result = {
        'epoc_time': str(datetime.datetime.utcnow().timestamp() * 1000),
        'argmax_index': int(np.argmax(scores)),
        'value_at_argmax': str(scores[np.argmax(scores)].numpy()),
        'class': classifier['meta']['classes'][np.argmax(scores)],
        'classes': classifier['meta']['classes'],
        'scores': scores.numpy().tolist(),
        'id': id,
        'image_saved': 0,
        'model_name': model_name
    }

    save_image(id, original_image, classifier, model_name, result)

    return result
