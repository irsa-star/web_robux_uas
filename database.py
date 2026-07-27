import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="lijzak.h.filess.io",
            user="db_robux_production",
            password="96afcc7d2e0ffee27e7921b632c858d75ca85a03",  
            database="db_robux_production",
            port="3305"   
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error saat menyambung ke database: {e}")
        return None
