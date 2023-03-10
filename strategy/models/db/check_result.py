import config_auth
from strategy.models.db.conn_db import conn_db
from strategy.controllers.convert_data.convert_datetime import datetime_now


def update_database_M5(obj_database, lista_padroes):
    conn = conn_db()
    cursor = conn.cursor()
    print(" **** DB - CONECTADO **** ")
    # 'id', 'open_time', 'active', 'direction', 'resultado', 'padrao', 'alert_datetime', 'expiration_alert', 'expiration_alert_timestamp', 'status_alert', 'name_strategy', 'mercado', 'alert_time_update'
    
    try:
        
        for df in obj_database:
            print("\n\n------------------------ dataframe update --------------------------------")
            print(df[["active_name", "status_candle", "from"]])

            active              = df["active_name"][0].split()[0]
            status_candle       = df["status_candle"][0]
            expiration_alert    = df["from"][0]

            
            # lista_padroes = ["V1", "V2", "V3", "V4"]
            for p in lista_padroes:
                padrao = f"PADRAO-M5-{p}"
                print(f"------->> active: {active} | status_candle: {status_candle} | padrão: {padrao} | expiration_alert: {expiration_alert}")
                comando_query = f'''
                SELECT direction, active, resultado, padrao, expiration_alert  FROM {config_auth.TABLE_NAME_M5}
                WHERE
                active = "{active}" and padrao = "{padrao}" and expiration_alert = "{expiration_alert}"
                '''
                cursor.execute(comando_query)
                result_query = cursor.fetchall()
                print(f"\n\n\n############ QUERY UPDATE: {result_query}")

                tt_query = len(result_query)
                print(f"\n\n --->> Total registros check results: {tt_query}")
                if tt_query >= 1:
                    direcao = result_query[0][1]
                    resultado = None

                    if status_candle == "sem mov.":
                        resultado = "empate"
                    elif status_candle != "sem mov." and status_candle != direcao:
                        resultado = "loss"
                    elif status_candle == direcao:
                        resultado = "win"
                    else:
                        resultado = "-"
                    
                    print(f" ######### Direção: {direcao} | Resultado: {resultado} #########")
                    alert_time_update = datetime_now(tzone="America/Sao Paulo")
                    
                    comando_update = f'''
                    UPDATE FROM {config_auth.TABLE_NAME_M5}
                    SET resultado = "{resultado}", alert_time_update = "{alert_time_update}"
                    WHERE active = "{active}" and padrao = "{padrao}" and expiration_alert = "{expiration_alert}" and id >= 0
                    '''
                    cursor.execute(comando_update)
                    conn.commit()
                    print(comando_update)
                    print(" ****** Registro atualizado com sucesso. Database desconectado. ****** ")
        
        cursor.close()
        conn.close()
        print(" *** DB - DESCONECTADO | UPDATE RESULT *** ")

    except Exception as e:
        print(f"\n\n ############### Erro UPDATE: {e}\n\n\n")
        try:
            # print(id_df)
            cursor.close()
            conn.close()
            print(" *** DB - DESCONECTADO | UPDATE RESULT *** ")
        except Exception as e_db:
            print(f"ErroDB Close: {e_db}")