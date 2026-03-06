<!DOCTYPE html>
<html>
<head>
    <title>Rice Prediction</title>
</head>
<body>

<h2>Upload Rice Image & Choose Model</h2>

<input type="file" id="fileInput"><br><br>

<select id="modelSelect">
    <option value="">-- Select Model --</option>
    <option value="DenseNet121">DenseNet121</option>
    <option value="MobileNet">MobileNet</option>
</select>

<br><br>
<button onclick="predictImage()">Predict</button>

<h3>Prediction Output:</h3>
<pre id="output"></pre>

<h3>Image Preview:</h3>
<img id="preview" width="250" style="display:none;">

<script>
function predictImage() {
    let file = document.getElementById("fileInput").files[0];
    let model = document.getElementById("modelSelect").value;

    if (!file) {
        alert("Upload an image.");
        return;
    }
    if (!model) {
        alert("Select a model.");
        return;
    }

    let form = new FormData();
    form.append("file", file);
    form.append("model_choice", model);   // FIXED

    // Preview image
    let reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById("preview").src = e.target.result;
        document.getElementById("preview").style.display = "block";
    };
    reader.readAsDataURL(file);

    fetch("http://127.0.0.1:5000/predict", {   // FIXED
        method: "POST",
        body: form
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").textContent =
            JSON.stringify(data, null, 4);
    })
    .catch(err => {
        document.getElementById("output").textContent = "Error: " + err;
    });
}
</script>

</body>
</html>
