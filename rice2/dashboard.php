<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Dashboard | Rice Varieties Identification</title>

<!-- Font Awesome Icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<style>
body{
    font-family: Arial, sans-serif;
    background:#f4f6f8;
}

/* CARD */
.container{
    width:650px;
    margin:70px auto;
    background:#ffffff;
    padding:30px;
    border-radius:12px;
    box-shadow:0 6px 18px rgba(0,0,0,0.2);
    text-align:center;
}

/* LOGO */
.logo-box img{
    width:130px;
}
.logo-box h3{
    color:#2e7d32;
    margin:10px 0 20px;
}

/* GRID */
.grid{
    display:grid;
    grid-template-columns:repeat(3,1fr); /* UPDATED */
    gap:20px;
    margin-top:20px;
}

/* BUTTON CARDS */
.card{
    padding:20px;
    border-radius:10px;
    text-decoration:none;
    color:#ffffff;
    font-size:18px;
    transition:0.3s;
}

.card i{
    font-size:35px;
    margin-bottom:10px;
    display:block;
}

/* COLORS */
.register{background:#1976d2;}
.login{background:#00796b;}
.predict{background:#2e7d32;}
.history{background:#6a1b9a;}
.logout{background:#c62828;}

.card:hover{
    transform:scale(1.05);
    opacity:0.95;
}

p{
    margin-top:10px;
    color:#333;
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

    <p>Welcome, <b><?php echo $_SESSION['username']; ?></b></p>

    <div class="grid">

        <a href="register.php" class="card register">
            <i class="fa-solid fa-user-plus"></i>
            Register
        </a>

        <a href="login.php" class="card login">
            <i class="fa-solid fa-right-to-bracket"></i>
            Login
        </a>

        <a href="predict.html" class="card predict">
            <i class="fa-solid fa-seedling"></i>
            Predict Rice
        </a>

        <a href="logout.php" class="card logout">
            <i class="fa-solid fa-arrow-right-from-bracket"></i>
            Logout
        </a>

    </div>

</div>

</body>
</html>
