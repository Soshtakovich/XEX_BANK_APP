import mysql.connector
import pymysql.cursors

db_config = {
    'user': '#############',
    'password': '############',
    'host': 'sql56.jnb2.host-h.net',
    'database': 'asdbanking',
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

