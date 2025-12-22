# File: app.py

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from functools import wraps
import time

# Impor konfigurasi
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# --- Fungsi Koneksi Database ---

def get_db_connection():
    """
    Membuka koneksi database MySQL.
    Menggunakan koneksi tunggal (tanpa pooling) untuk menghindari error impor 'pooling'.
    """
    try:
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return conn
    except mysql.connector.Error as err:
        print("-" * 50)
        print(f"ERROR KRITIS: Gagal terhubung ke database.")
        print(f"Detail Error: {err}")
        print("Pastikan XAMPP (MySQL) berjalan dan database 'balladigital' sudah dibuat.")
        print("-" * 50)
        return None

# --- Decorator untuk Proteksi Halaman ---
def login_required(f):
    """Mendekorasi fungsi view agar memerlukan autentikasi sesi."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Anda harus login terlebih dahulu.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Rute Autentikasi ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Menangani permintaan login pengguna."""
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn is None:
            # Jika koneksi gagal, tampilkan pesan yang jelas
            flash('Gagal terhubung ke database. Cek konfigurasi MySQL di XAMPP dan pastikan database telah dibuat.', 'danger')
            return render_template('login.html', username=username)

        user = None
        password_matches = False # Inisialisasi
        
        try:
            cursor = conn.cursor(dictionary=True)
            # Ambil data pengguna berdasarkan username
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
        except mysql.connector.Error as err:
            flash(f'Terjadi kesalahan saat mengambil data dari database: {err}', 'danger')
            return render_template('login.html', username=username)
        finally:
            conn.close() # Pastikan koneksi ditutup/dikembalikan

        # --- DEBUGGING: Cek Status Hash ---
        print(f"\n--- DEBUG LOGIN ATTEMPT ---")
        print(f"Username Attempted: {username}")
        
        if user:
            print(f"User found in DB (ID: {user['id']}).")
            # --- Verifikasi Password ---
            password_matches = check_password_hash(user['password'], password)
            print(f"check_password_hash result: {password_matches}")
        else:
            print("User NOT found in database.")
        print(f"---------------------------\n")

        
        if user and password_matches:
            # Login berhasil
            session['logged_in'] = True
            session['username'] = user['username']
            session['user_id'] = user['id']
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Login gagal
            flash('Username atau Password salah. (Petunjuk: admin / admin123)', 'danger')
            return render_template('login.html', username=username)

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Menghapus sesi pengguna dan mengarahkan ke halaman login."""
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('user_id', None)
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('login'))

# --- Rute Utama (Memerlukan Login) ---

@app.route('/')
@login_required
def index():
    """Rute default, mengarahkan ke dashboard."""
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Halaman Beranda/Dashboard."""
    return render_template('dashboard.html', active_menu='beranda')

@app.route('/data-iklan')
@login_required
def data_iklan():
    """Halaman Data Iklan."""
    return render_template('data_iklan.html', active_menu='data_iklan')

@app.route('/laporan')
@login_required
def laporan():
    """Halaman Laporan."""
    return render_template('laporan.html', active_menu='laporan')


if __name__ == '__main__':
    # Catatan: Jika gagal login, cek output di konsol terminal Flask.
    # Jika hash password bermasalah, jalankan 'generate_hash.py' untuk mendapatkan hash baru.
    app.run(debug=True)