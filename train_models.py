# Training script for DenseNet121 and MobileNetV2 on rice dataset
import tensorflow as tf
from tensorflow.keras.applications import DenseNet121, MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
import os, pathlib

img_size = (224, 224)
batch_size = 16
epochs = 3

# FIXED WINDOWS PATH (raw string)
dataset_dir = r"C:\xampp\htdocs\Full_Rice_Varieties_Project\full_rice_project\dataset"

# Check if dataset exists
if not os.path.exists(dataset_dir):
    raise FileNotFoundError(f"Dataset folder not found at: {dataset_dir}")

data_root = pathlib.Path(dataset_dir)

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_root, validation_split=0.2, subset="training", seed=123,
    image_size=img_size, batch_size=batch_size)

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_root, validation_split=0.2, subset="validation", seed=123,
    image_size=img_size, batch_size=batch_size)

class_names = train_ds.class_names
num_classes = len(class_names)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

def build_model(base_name):
    base = DenseNet121(weights='imagenet', include_top=False,
                       input_shape=(224, 224, 3)) if base_name == "DenseNet121" \
          else MobileNetV2(weights='imagenet', include_top=False,
                           input_shape=(224, 224, 3))

    x = GlobalAveragePooling2D()(base.output)
    x = Dropout(0.4)(x)
    x = Dense(256, activation='relu')(x)
    outputs = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base.input, outputs=outputs)

    for layer in base.layers[:-50]:
        layer.trainable = False

    model.compile(optimizer=Adam(learning_rate=1e-4),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

print("\nTraining DenseNet121...")
model1 = build_model("DenseNet121")
model1.fit(train_ds, validation_data=val_ds, epochs=epochs)
model1.save("DenseNet121_rice_model.h5")

print("\nTraining MobileNetV2...")
model2 = build_model("MobileNetV2")
model2.fit(train_ds, validation_data=val_ds, epochs=epochs)
model2.save("MobileNetV2_rice_model.h5")

print("\nTraining complete. Models saved.")
