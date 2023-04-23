import numpy as np
import tensorflow as tf
import pathlib

from PIL import Image, ImageDraw

from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from sklearn.metrics import confusion_matrix
from sklearn.utils.class_weight import compute_class_weight

def build_and_train(root_image_directory, model_location,
                    model_name, epochs=10,
                    resize_ratio=0.2, auto_balance_data=True):
    data_dir = pathlib.Path(root_image_directory)

    image_list = list(data_dir.glob('*/*.png'))
    image_count = len(image_list)
    print(image_count)

    img = Image.open(image_list[0])

    batch_size = 1
    img_height = int(img.height * resize_ratio)
    img_width = int(img.width * resize_ratio)

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    class_names = train_ds.class_names
    print(f"Class Names: {class_names}")

    class_weights = None
    if auto_balance_data:
        y_train = np.concatenate([y for x, y in train_ds], axis=0)

        class_weights = compute_class_weight(class_weight="balanced", classes=np.unique(y_train), y=y_train)
        class_weights = {i: w for i, w in enumerate(class_weights)}

        print(f"Class Weights: {class_weights}")




    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    num_classes = len(class_names)

    model = Sequential([
        layers.Rescaling(1. / 255, input_shape=(img_height, img_width, 3)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        class_weight=class_weights
    )
    train_data = list(train_ds)
    features = np.concatenate([train_data[n][0] for n in range(0, len(train_data))])
    targets = np.concatenate([train_data[n][1] for n in range(0, len(train_data))])
    print(targets)
    predictions = model.predict(features)
    print(predictions.argmax(1))

    cf = confusion_matrix(targets, predictions.argmax(1).astype(int))

    model.save(model_location)

    stats = {
        'cm': cf
    }
    rendering = {
        'image_resize': [img_height, img_width],
        'classes': class_names
    }

    return stats, rendering
