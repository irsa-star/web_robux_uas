@app.route('/leaderboard')
def leaderboard():
    cursor = mysql.connection.cursor()
    
    # Menaruh query SQL
    sql = """
        SELECT 
            u.username, 
            COUNT(t.id) AS total_transaksi, 
            SUM(p.nominal_robux) AS total_robux_dibeli
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        JOIN products p ON t.product_id = p.id
        WHERE t.status = 'success'
        GROUP BY u.id
        ORDER BY total_robux_dibeli DESC
        LIMIT 10
    """
    
    cursor.execute(sql)
    top_spenders = cursor.fetchall()
    
    # Mengirim data ke file HTML (Jinja2)
    return render_template('leaderboard.html', data=top_spenders)