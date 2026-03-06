# train_rice_models.py
# Train DenseNet121 & MobileNetV2 on rice varieties dataset

import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.applications import DenseNet121, MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
import pathlib, os

# ---------------- SETTINGS ----------------
img_size = (224, 224)
batch_size = 16
epochs = 10  # Increase to 20 or 30 for better accuracy
dataset_dir = "dataset"   # <-- your rice dataset folder

# ---------------- LOAD DATASET ----------------
if not os.path.exists(dataset_dir):
    raise FileNotFoundError(
        "❌ Dataset folder not found. Place rice images inside 'dataset/' folder."
    )

data_root = pathlib.Path(dataset_dir)

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_root,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_root,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

# Class names
class_names = train_ds.class_names
num_classes = len(class_names)
print("\n📌 Classes detected:", class_names)

# Performance optimization
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

# ---------------- MODEL BUILDER ----------------
def build_model(base_name):
    base = DenseNet121(weights="imagenet", include_top=False, input_shape=(224, 224, 3)) \
        if base_name == "DenseNet121" else \
        MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

    x = GlobalAveragePooling2D()(base.output)
    x = Dropout(0.4)(x)
    x = Dense(256, activation="relu")(x)
    outputs = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base.input, outputs=outputs)

    # Freeze base layers
    for layer in base.layers[:-50]:
        layer.trainable = False

    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

# ---------------- TRAIN MODELS ----------------
print("\n🔥 Training DenseNet121...")
densenet = build_model("DenseNet121")
densenet.fit(train_ds, validation_data=val_ds, epochs=epochs)
densenet.save("DenseNet121_rice_model.h5")
print("✔ DenseNet121 Model Saved!")

print("\n🔥 Training MobileNetV2...")
mobilenet = build_model("MobileNetV2")
mobilenet.fit(train_ds, validation_data=val_ds, epochs=epochs)
mobilenet.save("MobileNetV2_rice_model.h5")
print("✔ MobileNetV2 Model Saved!")

print("\n🎉 Training Complete! Models saved successfully.")
