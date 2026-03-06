import tensorflow as tf
from tensorflow.keras.applications import DenseNet121, MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image_dataset_from_directory
import pathlib

# ================= SETTINGS ==================
img_size = (224, 224)
batch_size = 16
epochs = 5
dataset_dir = 'dataset'   # MUST contain rice variety folders

# ================= LOAD DATASET ==================
data_root = pathlib.Path(dataset_dir)

train_ds = image_dataset_from_directory(
    data_root,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

val_ds = image_dataset_from_directory(
    data_root,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=img_size,
    batch_size=batch_size
)

class_names = train_ds.class_names
num_classes = len(class_names)

print("Rice Classes Found:", class_names)

# Improve performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)

# ================= BUILD MODEL FUNCTION ==================
def build_model(base_name):
    if base_name == "DenseNet121":
        base = DenseNet121(weights='imagenet', include_top=False, input_shape=(img_size[0], img_size[1], 3))
    else:
        base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(img_size[0], img_size[1], 3))

    x = GlobalAveragePooling2D()(base.output)
    x = Dropout(0.4)(x)
    x = Dense(256, activation='relu')(x)
    outputs = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base.input, outputs=outputs)

    # Freeze most layers
    for layer in base.layers[:-50]:
        layer.trainable = False

    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

# ================= TRAINING ==================
print("\nTraining DenseNet121...")
densenet = build_model("DenseNet121")
densenet.fit(train_ds, validation_data=val_ds, epochs=epochs)
densenet.save("DenseNet121_rice.h5")

print("\nTraining MobileNetV2...")
mobilenet = build_model("MobileNetV2")
mobilenet.fit(train_ds, validation_data=val_ds, epochs=epochs)
mobilenet.save("MobileNetV2_rice.h5")

print("\nTraining Complete! Models Saved.")
