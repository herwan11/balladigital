# /app.py
# Backend utama menggunakan Flask dan MySQL (XAMPP)

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'balla_digital_key_senior'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="balladigital"
    )

@app.route('/')
def index():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        flash('Username atau Password salah!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ads ORDER BY start_datetime ASC")
    ads_data = cursor.fetchall()
    cursor.close()
    conn.close()
    for ad in ads_data:
        ad['start_datetime'] = ad['start_datetime'].isoformat()
        ad['stop_datetime'] = ad['stop_datetime'].isoformat()
    return render_template('dashboard.html', ads=ads_data)

@app.route('/ads')
def ads_page():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ads ORDER BY created_at DESC")
    ads_list = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Perbaikan: Konversi datetime ke string ISO agar bisa diproses oleh tojson di template
    for ad in ads_list:
        if isinstance(ad['start_datetime'], datetime):
            ad['start_datetime'] = ad['start_datetime'].isoformat()
        if isinstance(ad['stop_datetime'], datetime):
            ad['stop_datetime'] = ad['stop_datetime'].isoformat()
            
    return render_template('ads.html', ads=ads_list)

@app.route('/ads/save', methods=['POST'])
def save_ads():
    ad_id = request.form.get('id')
    nama = request.form.get('nama_ads')
    budget = request.form.get('budget_harian')
    
    # Logika Akumulasi Durasi
    durasi_awal = int(request.form.get('durasi_hari') or 0)
    tambahan = int(request.form.get('tambah_durasi') or 0)
    total_durasi = durasi_awal + tambahan
    
    start_str = request.form.get('start_datetime')
    try:
        # Parsing format dari datetime-local (YYYY-MM-DDTHH:MM)
        start_dt = datetime.strptime(start_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        # Fallback jika format berbeda
        start_dt = datetime.fromisoformat(start_str.replace(' ', 'T'))

    # Ambil waktu saat ini untuk menetapkan jam berakhir (sesuai instruksi)
    now = datetime.now()
    
    # Hitung Tanggal Berakhir berdasarkan Total Durasi
    stop_dt_base = start_dt + timedelta(days=total_durasi)
    
    # Atur jam dan menit agar mengikuti waktu saat tombol simpan ditekan
    stop_dt = stop_dt_base.replace(hour=now.hour, minute=now.minute, second=0)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if ad_id:
        # Update data lama dengan durasi kumulatif dan jam berakhir baru
        query = "UPDATE ads SET nama_ads=%s, budget_harian=%s, durasi_hari=%s, start_datetime=%s, stop_datetime=%s WHERE id=%s"
        cursor.execute(query, (nama, budget, total_durasi, start_dt, stop_dt, ad_id))
    else:
        # Input iklan baru
        query = "INSERT INTO ads (nama_ads, budget_harian, durasi_hari, start_datetime, stop_datetime) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nama, budget, total_durasi, start_dt, stop_dt))
        
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('ads_page'))

@app.route('/ads/delete/<int:id>')
def delete_ads(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ads WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('ads_page'))

if __name__ == '__main__':
    app.run(debug=True)