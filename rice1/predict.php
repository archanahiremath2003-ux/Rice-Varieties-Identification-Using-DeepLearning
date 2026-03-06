<?php
session_start();
include('db.php');

if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}

$userStmt = mysqli_prepare($conn, "SELECT id FROM users WHERE username = ? LIMIT 1");
mysqli_stmt_bind_param($userStmt, "s", $_SESSION['username']);
mysqli_stmt_execute($userStmt);
mysqli_stmt_bind_result($userStmt, $user_id);
mysqli_stmt_fetch($userStmt);
mysqli_stmt_close($userStmt);

$prediction = "";
$uploaded_image_path = "";

if (isset($_POST['submit'])) {

    $model_choice = $_POST['model_choice'];

    if (!isset($_FILES['file']) || $_FILES['file']['error'] != 0) {
        $prediction = "Please upload a valid image.";
    } else {

        $uploads_dir = 'uploads/';
        if (!file_exists($uploads_dir)) { mkdir($uploads_dir, 0777, true); }

        $filename = time() . "_" . basename($_FILES['file']['name']);
        $target = $uploads_dir . $filename;

        if (move_uploaded_file($_FILES['file']['tmp_name'], $target)) {

            $uploaded_image_path = $target;

            $api_url = "http://127.0.0.1:5000/predict";
            $cfile = new CURLFile($target, mime_content_type($target), $filename);

            $post = array(
                'file' => $cfile,
                'model' => $model_choice
            );

            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $api_url);
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

            $response = curl_exec($ch);
            curl_close($ch);

            $result = json_decode($response, true);

            if (!$result) {
                $prediction = "Error: Invalid JSON from model server.<br>Response: " . htmlspecialchars($response);
            } else if (isset($result['error'])) {
                $prediction = "Error: " . $result['error'];
            } else {
                $prediction = 
                    "<strong>Model Used:</strong> " . $result['model_used'] . "<br>" .
                    "<strong>Prediction:</strong> " . $result['prediction'] . "<br>" .
                    "<strong>Confidence:</strong> " . $result['confidence'];
            }

            $stmt = mysqli_prepare($conn, "INSERT INTO uploads (user_id, filename, model_choice) VALUES (?, ?, ?)");
            mysqli_stmt_bind_param($stmt, "iss", $user_id, $filename, $model_choice);
            mysqli_stmt_execute($stmt);
            mysqli_stmt_close($stmt);

        } else {
            $prediction = "Failed to upload image.";
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Rice Image Prediction</title>
<style>
body{font-family:Arial;background:#eef2f3;padding:30px;}
.card{background:#fff;padding:25px;border-radius:10px;max-width:600px;margin:auto;box-shadow:0 4px 15px rgba(0,0,0,0.1);}
.btn{background:#4a90e2;color:#fff;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;}
.btn:hover{background:#357abd;}
.preview-img{margin-top:20px;display:block;border-radius:10px;max-width:250px;}
.result-box{margin-top:20px;padding:15px;background:#f0fff4;border-left:5px solid #2e7d32;border-radius:5px;}
</style>
</head>
<body>
<div class="card">
<h2>Welcome, <?php echo htmlspecialchars($_SESSION['username']); ?> 👋</h2>
<h3>Upload Rice Image & Predict Variety</h3>

<form method="POST" enctype="multipart/form-data">
    <label>Select Image:</label><br>
    <input type="file" name="file" accept="image/*" required><br><br>

    <label>Select Model:</label><br>
    <select name="model_choice" required>
        <option value="">-- Choose Model --</option>
        <option value="DenseNet121">DenseNet121</option>
        <option value="MobileNet">MobileNet</option>
    </select><br><br>

    <button type="submit" name="submit" class="btn">Predict</button>
</form>

<img id="preview" class="preview-img" style="display:none;">

<script>
document.querySelector("input[type=file]").addEventListener("change", function(event) {
    let file = event.target.files[0];
    if (!file) return;
    let reader = new FileReader();
    reader.onload = function(e) {
        let img = document.getElementById("preview");
        img.src = e.target.result;
        img.style.display = "block";
    };
    reader.readAsDataURL(file);
});
</script>

<?php if ($uploaded_image_path): ?>
<h3>Uploaded Image:</h3>
<img src="<?php echo $uploaded_image_path; ?>" class="preview-img">
<?php endif; ?>

<?php if ($prediction): ?>
<div class="result-box">
<?php echo $prediction; ?>
</div>
<?php endif; ?>

</div>
</body>
</html>
