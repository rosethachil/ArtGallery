import mysql.connector

def connect_to_db():  # connect to sql from python
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="roseliz@03",
        database="ArtGalleryDB"
    )
    return db

def fetch_data(query, params=None):
    connection = connect_to_db()
    cursor = connection.cursor()    #   this acts as pointer to db entries
    try: 
        cursor.execute(query, params or ())     
        data = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    return data


def execute_query(query, params=None,return_cursor=False):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        connection.commit()
        if return_cursor:
            return cursor
    finally:
        cursor.close()
        connection.close()
