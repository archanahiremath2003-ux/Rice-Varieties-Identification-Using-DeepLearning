<?php
session_start();
include('db.php');

if (isset($_POST['login'])) {
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $password = $_POST['password'];

    $stmt = mysqli_prepare($conn, "SELECT username, password FROM users WHERE email = ? LIMIT 1");
    mysqli_stmt_bind_param($stmt, "s", $email);
    mysqli_stmt_execute($stmt);
    mysqli_stmt_bind_result($stmt, $username, $hashed);
    mysqli_stmt_fetch($stmt);
    mysqli_stmt_close($stmt);

    if ($hashed && password_verify($password, $hashed)) {
        $_SESSION['username'] = $username;

        // ✅ Redirect to prediction page
        header("Location: predict.html");
        exit();
    } else {
        echo "<script>alert('Invalid email or password');</script>";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Rice Varieties Identification | Login</title>

<style>
body{
    background: linear-gradient(135deg,#e8f5e9,#ffffff);
    font-family: Arial, sans-serif;
}

.container{
    width:380px;
    margin:90px auto;
    background:#fff;
    padding:28px;
    border-radius:14px;
    box-shadow:0 10px 25px rgba(0,0,0,0.2);
}

.logo-box{
    text-align:center;
    margin-bottom:18px;
}

.logo-box img{
    width:140px;   /* BIG LOGO */
}

.logo-box h3{
    color:#2e7d32;
    margin-top:8px;
    font-size:22px;
}

h2{
    text-align:center;
    margin-bottom:20px;
}

input{
    width:100%;
    padding:12px;
    margin:10px 0;
    border-radius:6px;
    border:1px solid #ccc;
    font-size:15px;
}

button{
    width:100%;
    background:#2e7d32;
    color:#fff;
    padding:12px;
    border:none;
    border-radius:6px;
    font-size:16px;
    cursor:pointer;
}

button:hover{
    background:#1b5e20;
}

p{
    text-align:center;
    margin-top:15px;
}

a{
    color:#2e7d32;
    text-decoration:none;
    font-weight:bold;
}
</style>
</head>

<body>

<div class="container">

    <!-- LOGO -->
    <div class="logo-box">
        <img src="assets/logo.jpg" alt="Rice Logo">
        <h3>Rice Varieties Identification</h3>
    </div>

    <h2>Login</h2>

    <form method="POST" autocomplete="off">
        <input type="email" name="email" placeholder="Email" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit" name="login">Login</button>
    </form>

    <p>Don't have an account? <a href="register.php">Register</a></p>

</div>

</body>
</html>
