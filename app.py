import os
import pymysql
from flask import Flask, render_template, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=BASE_DIR, static_folder=BASE_DIR)

# Fungsi Koneksi ke file.io
def get_db_connection():
    return pymysql.connect(
        host='24hgxj.h.filess.io',
        user='db_greentoup_discoveris',
        port = "3305",
        password='7fad1090377a48955a3068fd6d61ef9b33e6bf87',
        database='db_greentoup_discoveris',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leaderboard ORDER BY rank ASC")
        data_leaderboard = cursor.fetchall()
        conn.close()
    except Exception as e:
        print("Gagal koneksi ke database:", e)
        data_leaderboard = []

    return render_template('index.html', leaderboard=data_leaderboard)

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)

if __name__ == '__main__':
    print("Server GreenTopUp berjalan di: http://127.0.0.1:5000")
    app.run(debug=True, port=5000) 
