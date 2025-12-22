-- File: sql/balladigital.sql

-- 1. Buat Database jika belum ada
CREATE DATABASE IF NOT EXISTS balladigital;
USE balladigital;

-- 2. Buat Tabel Users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    -- Kolom password akan menyimpan hash password
    password VARCHAR(255) NOT NULL
);

-- 3. Insert User Admin Default
-- Username: admin
-- Password: admin123 (Hash menggunakan werkzeug.security/pbkdf2:sha256:600000)
-- Jika Anda ingin mengganti password, Anda perlu menghasilkan hash baru.
INSERT INTO users (username, password) VALUES 
('admin', 'pbkdf2:sha256:600000$u32Lh3ZqB5xI7i1B$97669d511394c483f80c634d9894e772d1f7e3c15d4e13838e7456d6837894a8');

-- Selesai.
-- Setelah menjalankan skrip ini di MySQL, user 'admin' dengan password 'admin123' akan siap digunakan.