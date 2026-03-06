from tensorflow.keras.applications.densenet import preprocess_input as densenet_preprocess
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mobilenet_preprocess
from flask_cors import CORS
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
CORS(app)

DENSENET_PATH = r"C:\xampp\htdocs\Full_Rice_Varieties_Project\full_rice_project\models\DenseNet121_rice_model.h5"
MOBILENET_PATH = r"C:\xampp\htdocs\Full_Rice_Varieties_Project\full_rice_project\models\MobileNetV2_rice_model.h5"

for p in [DENSENET_PATH, MOBILENET_PATH]:
    if not os.path.exists(p):
        raise FileNotFoundError(f"Model file missing: {p}")

print("Loading models...")
densenet_model = tf.keras.models.load_model(DENSENET_PATH, compile=False)
mobilenet_model = tf.keras.models.load_model(MOBILENET_PATH, compile=False)
print("Models loaded successfully.")

CLASS_NAMES = ["Basmati", "jasmine", "Komal", "Ponni", "Sona-masoor"]

def preprocess(img, model_name):
    img = img.resize((224, 224))
    arr = np.array(img)

    if model_name == "DenseNet121":
        arr = densenet_preprocess(arr)
    else:
        arr = mobilenet_preprocess(arr)

    return np.expand_dims(arr, axis=0)

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
