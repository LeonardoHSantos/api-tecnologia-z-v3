import config_auth
from strategy.models.db.conn_db import conn_db


def insert_database_M5(obj_database):
    # 'id', 'open_time', 'active', 'direction', 'resultado', 'padrao', 'alert_datetime', 'expiration_alert', 'expiration_alert_timestamp', 'status_alert', 'name_strategy', 'mercado', 'alert_time_update'
    
    try:
        conn = None
        cursor = None
        try:
            conn = conn_db()
        except Exception as e:
            print(f"Erro com o banco de dados: {e}")
        if conn != None:
            cursor = conn.cursor()

            print(" **** DB - CONECTADO **** ")
            open_time                   = obj_database["open_time"]
            active                      = obj_database["active"]
            direction                   = obj_database["direction"]
            resultado                   = obj_database["resultado"]
            padrao                      = obj_database["padrao"]
            alert_datetime              = obj_database["alert_datetime"]
            expiration_alert            = obj_database["expiration_alert"]
            expiration_alert_timestamp  = obj_database["expiration_alert_timestamp"]
            status_alert                = obj_database["status_alert"]
            name_strategy               = obj_database["name_strategy"]
            mercado                     = obj_database["mercado"]
            alert_time_update           = obj_database["alert_time_update"]

            comando_query = f'''
            SELECT * FROM {config_auth.TABLE_NAME_M5}
            WHERE
            active = "{active}" and padrao = "{padrao}" and expiration_alert = "{expiration_alert}" and name_strategy = "{name_strategy}"
            '''
            cursor.execute(comando_query)
            result_query = cursor.fetchall()

            tt_query = len(result_query)
            print(f"\n\n --->> Total registros DB: {tt_query}")

            if status_alert == "alert-open-operation" and direction != "-":
                open_time = open_time
                resultado = "open"
            else:
                open_time = ""

            if tt_query == 0:
                try:
                    comando_insert = f'''
                    INSERT INTO {config_auth.TABLE_NAME_M5}
                    (open_time, active, direction, resultado, padrao, alert_datetime, expiration_alert, expiration_alert_timestamp, status_alert, name_strategy, mercado, alert_time_update)
                    VALUES
                    ("{open_time}", "{active}", "{direction}", "{resultado}", "{padrao}", "{alert_datetime}", "{expiration_alert}", "{expiration_alert_timestamp}", "{status_alert}", "{name_strategy}", "{mercado}", "{alert_time_update}")
                    '''
                    print(comando_insert)
                    cursor.execute(comando_insert)
                    conn.commit()
                    print(" --->> Registro inserido com sucesso!")
                except Exception as e:
                    print(f"Erro INSERT DATABASE: {e}")
            else:
                try:
                    comando_update = f'''
                    UPDATE {config_auth.TABLE_NAME_M5}
                    SET open_time = "{open_time}", resultado = "{resultado}", direction = "{direction}", status_alert = "{status_alert}", alert_time_update = "{alert_time_update}"
                    WHERE name_strategy = "{name_strategy}" and expiration_alert = "{expiration_alert}" and id >= 0
                    '''
                    cursor.execute(comando_update)
                    conn.commit()
                    print(comando_update)
                    print(" ****** Registro atualizado com sucesso. Database desconectado. ****** ")
                except Exception as e:
                    print(f"Erro UPDATE DATABASE: {e}")
            try:
                cursor.close()
                conn.close()
                print(" *** DB - DESCONECTADO *** ")
            except Exception as e:
                print(f"#1 - Erro database: {e}")

    except Exception as e:
        print(f"\n\n ############### Erro : {e}\n\n\n")
        try:
            # print(id_df)
            cursor.close()
            conn.close()
            print(" *** DB - DESCONECTADO *** ")
        except Exception as e_db:
            print(f"ErroDB Close: {e_db}")