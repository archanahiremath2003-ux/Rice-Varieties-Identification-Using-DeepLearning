CREATE DATABASE IF NOT EXISTS user_db;
USE user_db;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS uploads (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  filename VARCHAR(255),
  model_choice VARCHAR(100),
  upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- sample user: email=lakshmi@example.com password=12345
INSERT INTO users (username, email, password) VALUES ('Lakshmi','lakshmi@example.com','$2y$10$G6jhYv1n0OlxzEE5e2HNCObxOrxS0eZrHfFvRHR4xq4pCCAdyQG8S');