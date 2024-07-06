import mysql.connector
import pymysql.cursors

db_config = {
    'user': 'alx_banking',
    'password': 'Fernando072903',
    'host': 'sql56.jnb2.host-h.net',
    'database': 'banking',
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

# Example usage
if __name__ == "__main__":
    connection = get_db_connection()
    if connection.open:
        print("Connected to the database")
        connection.close()
