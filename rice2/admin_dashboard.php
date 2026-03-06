<?php
session_start();
include('db.php');

if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}

$sql = "SELECT uploads.id, users.username, uploads.filename, uploads.model_choice, uploads.upload_time 
        FROM uploads JOIN users ON uploads.user_id = users.id ORDER BY uploads.upload_time DESC";
$res = mysqli_query($conn, $sql);
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Admin Dashboard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="page-bg">
<div class="container card">
    <h2>Uploaded Files Dashboard</h2>
    <div class="table-wrap">
    <table class="styled-table">
        <thead>
            <tr>
                <th>User</th>
                <th>Filename</th>
                <th>Model</th>
                <th>Uploaded At</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
        <?php if (mysqli_num_rows($res) > 0): ?>
            <?php while ($row = mysqli_fetch_assoc($res)): ?>
                <tr>
                    <td><?php echo htmlspecialchars($row['username']); ?></td>
                    <td><?php echo htmlspecialchars($row['filename']); ?></td>
                    <td><?php echo htmlspecialchars($row['model_choice']); ?></td>
                    <td><?php echo htmlspecialchars($row['upload_time']); ?></td>
                    <td><a href="uploads/<?php echo rawurlencode($row['filename']); ?>" target="_blank">Download</a></td>
                </tr>
            <?php endwhile; ?>
        <?php else: ?>
            <tr><td colspan="5">No uploads yet.</td></tr>
        <?php endif; ?>
        </tbody>
    </table>
    </div>
    <div class="links">
        <a href="preview.php">⬅ Back</a> | <a href="logout.php">Logout</a>
    </div>
</div>
</body>
</html>