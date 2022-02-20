import mysql


def connect_to_db(address, username):
    mysql.connect()
    print("Connected")

    return mysql.connect()
