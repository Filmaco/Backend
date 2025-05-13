from flask_mysql_connector import MySQL

mysql = MySQL()

def db_init(app):
    app.config['MYSQL_USER'] = 'lara'
    app.config['MYSQL_PASSWORD'] = 'LaraVictoria123_@;'
    app.config['MYSQL_DATABASE'] = 'filmaco'
    app.config['MYSQL_HOST'] = '127.0.0.1'  
    app.config['MYSQL_PORT'] = 3306         

    mysql.init_app(app)