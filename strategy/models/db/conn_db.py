import mysql.connector
import config_auth

def conn_db():
    try:
        conn = mysql.connector.connect(
            host=config_auth.HOST_DB,
            user=config_auth.USER_DB,
            password=config_auth.PASSWORD_DB,
            database=config_auth.NAME_DB,
        )
        return conn
    except Exception as e:
        print(f"Erro com a conexão com o banco de dados: {e}")
        return None