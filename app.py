from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection

app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key = 'secret_key_bebas_diisi_apa_saja'

# 1. Halaman Beranda (Home & Top Up dalam 1 Halaman)
@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", products=products)

# 2. Proses Checkout
@app.route("/checkout", methods=["POST"])
def checkout():
    roblox_username = request.form.get("roblox_username")
    product_id = request.form.get("product_id")
    user_id = 1 

    if roblox_username and product_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (user_id, product_id, roblox_username, status) VALUES (%s, %s, %s, 'success')",
            (user_id, product_id, roblox_username)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
    return redirect(url_for("leaderboard"))

# 3. Halaman Leaderboard
@app.route("/leaderboard")
def leaderboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            t.roblox_username,
            SUM(p.robux_amount) AS total_robux,
            SUM(p.price) AS total_spent,
            COUNT(t.id) AS total_transactions
        FROM transactions t
        JOIN products p ON t.product_id = p.id
        WHERE t.status = 'success'
        GROUP BY t.roblox_username
        ORDER BY total_robux DESC
        LIMIT 10
    """
    cursor.execute(query)
    leaderboard_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("leaderboard.html", leaderboard=leaderboard_data)

# 4. Halaman Sign In
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return redirect(url_for("home"))
        else:
            return redirect(url_for("signin"))

    return render_template("signin.html")

# 5. Halaman Sign Up
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return redirect(url_for("signup"))

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("signin"))

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)