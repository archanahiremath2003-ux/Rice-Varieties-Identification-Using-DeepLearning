import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import os

# ------------------------------
# Dataset Path (UPDATE IF NEEDED)
# ------------------------------
DATASET_PATH = r"C:\xampp\htdocs\Full_Rice_Varieties_Project\full_rice_project\dataset"

# ------------------------------
# Output Model Path
# ------------------------------
OUTPUT_PATH = r"C:\xampp\htdocs\Full_Rice_Varieties_Project\full_rice_project\models\DenseNet121_rice_model.h5"

# ------------------------------
# Hyperparameters
# ------------------------------
IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 10

# ------------------------------
# Load Dataset
# ------------------------------
train_ds = image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

val_ds = image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names
num_classes = len(class_names)
print("Classes:", class_names)

# ------------------------------
# Build DenseNet121 Model
# ------------------------------
base_model = DenseNet121(weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
base_model.trainable = False  # Freeze layers for transfer learning

x = base_model.output
x = GlobalAveragePooling2D()(x)
output_layer = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output_layer)

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ------------------------------
# Train Model
# ------------------------------
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)

# ------------------------------
# Save Model
# ------------------------------
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
model.save(OUTPUT_PATH)

print(f"DenseNet121 model saved at: {OUTPUT_PATH}")
