import mysql.connector
import config_auth

def conn_db():
    conn = mysql.connector.connect(
        host=config_auth.HOST_DB,
        user=config_auth.USER_DB,
        password=config_auth.PASSWORD_DB,
        database=config_auth.NAME_DB,
    )
    return conn