import mysql.connector

def connect_to_db():    # Connect to MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="roseliz@03",
        database="ArtGalleryDB"
    )
    return db

# This function to execute SELECT queries
def fetch_data(query, params=None):
    connection = connect_to_db()
    cursor = connection.cursor()    #   acts as pointer to dbms entries
    cursor.execute(query, params or ())     
    data = cursor.fetchall()
    connection.close()
    return data

# This function to execute INSERT/UPDATE/DELETE queries
def execute_query(query, params=None):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(query, params or ())
    connection.commit()
    connection.close()
