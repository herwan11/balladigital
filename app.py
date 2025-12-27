# /app.py (Updated with Resume Features)
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
    durasi_awal = int(request.form.get('durasi_hari') or 0)
    tambahan = int(request.form.get('tambah_durasi') or 0)
    total_durasi = durasi_awal + tambahan
    start_str = request.form.get('start_datetime')
    try:
        start_dt = datetime.strptime(start_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        start_dt = datetime.fromisoformat(start_str.replace(' ', 'T'))
    now = datetime.now()
    stop_dt_base = start_dt + timedelta(days=total_durasi)
    stop_dt = stop_dt_base.replace(hour=now.hour, minute=now.minute, second=0)
    conn = get_db_connection()
    cursor = conn.cursor()
    if ad_id:
        query = "UPDATE ads SET nama_ads=%s, budget_harian=%s, durasi_hari=%s, start_datetime=%s, stop_datetime=%s WHERE id=%s"
        cursor.execute(query, (nama, budget, total_durasi, start_dt, stop_dt, ad_id))
    else:
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

# --- FITUR RESUME BARU ---

@app.route('/resume')
def resume_page():
    if 'user_id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nama_ads FROM ads ORDER BY nama_ads ASC")
    ads_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('resume.html', ads_list=ads_list)

@app.route('/resume/data/<int:ad_id>')
def get_resume_data(ad_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Ambil data ads detail
    cursor.execute("SELECT * FROM ads WHERE id = %s", (ad_id,))
    ad_info = cursor.fetchone()
    # Ambil data report harian
    cursor.execute("SELECT * FROM ad_reports WHERE ad_id = %s ORDER BY report_date ASC", (ad_id,))
    reports = cursor.fetchall()
    cursor.close()
    conn.close()
    # Format date ke string
    for r in reports:
        r['report_date'] = r['report_date'].strftime('%Y-%m-%d')
    return jsonify({'ad': ad_info, 'reports': reports})

@app.route('/resume/save_report', methods=['POST'])
def save_report():
    data = request.json
    ad_id = data.get('ad_id')
    date = data.get('report_date')
    reach = data.get('reach', 0)
    impressions = data.get('impressions', 0)
    leads = data.get('leads', 0)
    spend = data.get('amount_spent', 0)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    # On Duplicate Key Update (UPSERT)
    query = """
        INSERT INTO ad_reports (ad_id, report_date, reach, impressions, leads, amount_spent)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE reach=%s, impressions=%s, leads=%s, amount_spent=%s
    """
    cursor.execute(query, (ad_id, date, reach, impressions, leads, spend, reach, impressions, leads, spend))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)