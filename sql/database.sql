-- Membuat database baru jika belum ada
CREATE DATABASE IF NOT EXISTS web_robux_uas;
USE web_robux_uas;

-- 1. Tabel Pengguna (Users)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabel Paket Robux (Products)
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    robux_amount INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabel Transaksi (Transactions)
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    roblox_username VARCHAR(100) NOT NULL, -- Username tujuan top-up
    status ENUM('pending', 'success', 'failed') DEFAULT 'pending',
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Menambahkan Data Dummy Awal (Opsional untuk Testing)
INSERT INTO products (name, robux_amount, price) VALUES
('Paket Hemat', 80, 15000),
('Paket Standar', 400, 75000),
('Paket Sultan', 800, 145000);