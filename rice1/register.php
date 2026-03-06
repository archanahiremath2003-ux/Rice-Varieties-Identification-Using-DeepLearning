<?php
include('db.php');
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rice Varieties Identification | Register</title>

    <style>
        body {
            background: #f4f6f8;
            font-family: Arial, sans-serif;
        }

        .container {
            width: 380px;
            margin: 80px auto;
            background: #fff;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        .logo-box {
            text-align: center;
            margin-bottom: 15px;
        }

        .logo-box img {
            width: 90px;
        }

        h3 {
            color: #2e7d32;
            margin-top: 8px;
        }

        input {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 5px;
            border: 1px solid #ccc;
        }

        button {
            width: 100%;
            background: #2e7d32;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #256428;
        }

        p {
            text-align: center;
        }

        a {
            color: #2e7d32;
            text-decoration: none;
        }
    </style>
</head>

<body>

<div class="container">

    <!-- REAL IMAGE LOGO -->
    <div class="logo-box">
        <img src="assets/logo.jpg" alt="Rice Logo">
        <h3>Rice Varieties Identification</h3>
    </div>

    <h2 style="text-align:center;">Register</h2>

    <form method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="email" name="email" placeholder="Email" required>
        <input type="password" name="password" placeholder="Password" required>
        <input type="password" name="confirm_password" placeholder="Confirm Password" required>
        <button type="submit" name="register">Register</button>
    </form>

    <p>Already have an account? <a href="login.php">Login</a></p>

</div>

</body>
</html>
