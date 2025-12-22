# File: config.py

class Config:
    """Class konfigurasi utama untuk aplikasi Flask."""
    SECRET_KEY = 'kunci-rahasia-yang-sangat-kuat-dan-sulit-ditebak'  # Ganti dengan kunci rahasia yang lebih aman
    
    # Konfigurasi Database MySQL (XAMPP default)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # Password kosong sesuai permintaan
    MYSQL_DB = 'balladigital'