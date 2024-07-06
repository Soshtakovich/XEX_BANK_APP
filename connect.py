import mysql.connector
import pymysql.cursors

db_config = {
    'user': '###########',
    'password': '############',
    'host': 'localhost',
    'database': 'alx_banking',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        cursorclass=db_config['cursorclass']
    )
