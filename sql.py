from getpass import getpass
from mysql.connector import connect, Error


m_user = 'root'
m_password = 'krekan123'
m_database = 'db_tass'
m_host = 'localhost'

def get_last_id(name_ch):
    last_id = 0
    with connect(
            host=m_host,
            user=m_user,
            password=m_password,
            database=m_database
    ) as connection:
        with connection.cursor() as cursor:
            try:
                query = "SELECT id FROM posts WHERE name='" + name_ch + "' ORDER BY ID DESC LIMIT 1"
                cursor.execute(query)
                records = cursor.fetchone()
                last_id = records[0]
                cursor.close()
                connection.close()
            except:
                last_id = 0

    return last_id


def save_msgs(msgs):
    try:
        with connect(
                host=m_host,
                user=m_user,
                password=m_password,
                database=m_database
        ) as connection:
            with connection.cursor() as cursor:
                createTable = """CREATE TABLE IF NOT EXISTS posts (
                                        id INT,
                                        name VARCHAR(500), 
                                        views INT,
                                        text VARCHAR(4096),                                        
                                        date DATETIME)"""
                cursor.execute(createTable)
                connection.commit()

                insert_query = "INSERT INTO posts (id, name, views, text, date) VALUES ( %s, %s, %s, %s, %s )"
                cursor.executemany(insert_query, msgs)
                connection.commit()
                cursor.close()
                connection.close()

    except Error as e:
        print(e)

