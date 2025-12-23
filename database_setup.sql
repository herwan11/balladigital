-- File: database_setup.sql
-- Deskripsi: Skema database balladigital untuk sistem manajemen iklan

CREATE DATABASE IF NOT EXISTS balladigital;
USE balladigital;

-- Tabel Users untuk sistem login sederhana
CREATE TABLE IF NOT EXISTS users (
id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(50) NOT NULL UNIQUE,
password VARCHAR(100) NOT NULL -- TANPA HASH sesuai permintaan
);

-- Tabel Ads untuk menyimpan data iklan
CREATE TABLE IF NOT EXISTS ads (
id INT AUTO_INCREMENT PRIMARY KEY,
nama_ads VARCHAR(100) NOT NULL,
budget_harian INT NOT NULL,
durasi_hari INT NOT NULL,
start_datetime DATETIME NOT NULL,
stop_datetime DATETIME NOT NULL,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert User Default untuk testing
INSERT INTO users (username, password) VALUES ('admin', 'admin123');

-- Insert Dummy Ads untuk melihat visualisasi kalender awal
INSERT INTO ads (nama_ads, budget_harian, durasi_hari, start_datetime, stop_datetime)
VALUES ('Promo Akhir Tahun', 50000, 7, '2023-12-23 08:00:00', '2023-12-30 08:00:00');