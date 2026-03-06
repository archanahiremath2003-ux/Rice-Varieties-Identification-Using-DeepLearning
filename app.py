from flask_cors import CORS
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import os
from tensorflow.keras.applications.densenet import preprocess_input as densenet_preprocess
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mobilenet_preprocess

app = Flask(__name__)
CORS(app)

# -------------------
# MODEL PATHS
# -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DENSENET_PATH = os.path.join(BASE_DIR, "..", "models", "DenseNet121_rice_model.h5")
MOBILENET_PATH = os.path.join(BASE_DIR, "..", "models", "MobileNetV2_rice_model.h5")

# -------------------
# LOAD MODELS
# -------------------
if not os.path.exists(DENSENET_PATH) or not os.path.exists(MOBILENET_PATH):
    raise FileNotFoundError("One or both model files are missing in the models/ folder.")

densenet_model = tf.keras.models.load_model(DENSENET_PATH, compile=False)
mobilenet_model = tf.keras.models.load_model(MOBILENET_PATH, compile=False)

CLASS_NAMES = ["Basmati", "Jasmine", "Komal", "Ponni", "Sona-masoor"]

# -------------------
# IMAGE PREPROCESS
# -------------------
def preprocess(img, model_name):
    img = img.resize((224, 224))
    arr = np.array(img)
    if model_name == "DenseNet121":
        arr = densenet_preprocess(arr)
    else:
        arr = mobilenet_preprocess(arr)
    arr = np.expand_dims(arr, 0)
    return arr

# -------------------
# PREDICT ROUTE
# -------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        file = request.files.get("file")
        model_choice = request.form.get("model_choice")

        if not file:
            return jsonify({"error": "No file uploaded"}), 400
        if model_choice not in ["DenseNet121", "MobileNet"]:
            return jsonify({"error": "Invalid model choice"}), 400

        img = Image.open(file)
        arr = preprocess(img, model_choice)

        if model_choice == "DenseNet121":
            pred = densenet_model.predict(arr)
        else:
            pred = mobilenet_model.predict(arr)

        idx = int(np.argmax(pred))
        conf = float(pred[0][idx])

        return jsonify({
            "model_used": model_choice,
            "prediction": CLASS_NAMES[idx],
            "confidence": round(conf, 4)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
