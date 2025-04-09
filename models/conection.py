import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",         
        port=3306,                
        user="lara",
        password="LaraVictoria123_@;",
        database="filmaco"
    )