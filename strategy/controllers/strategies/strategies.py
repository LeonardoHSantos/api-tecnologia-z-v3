import pandas as pd

from strategy.models.db.insert import insert_database_M5


# from strategy.controllers.strategies.process_data_sup_res import Check_sup_res
from strategy.controllers.convert_data.convert_datetime import expiration_operation_M5, expiration_operation_M5_2
from strategy.var_data_aux import LIST_MINUTES_STRATEGY_V1, LIST_MINUTES_STRATEGY_V2, LIST_MINUTES_STRATEGY_V3, LIST_MINUTES_STRATEGY_V4


def prepare_message_database(active, direction, resultado, padrao, status_alert, name_strategy, mercado, t_version):
    expiration_5m = None
    if t_version == "M5-V3":
        expiration_5m = expiration_operation_M5_2(tzone="America/Sao Paulo")
    else:
        expiration_5m = expiration_operation_M5_2(tzone="America/Sao Paulo")

    obj_msg_database = {
        "open_time"                       : expiration_5m["open_time"],
        "active"                          : active,
        "direction"                       : direction,
        "resultado"                       : resultado,
        "padrao"                          : padrao,
        "alert_datetime"                  : expiration_5m["alert_datetime"],
        "expiration_alert"                : expiration_5m["expiration_alert"],
        "expiration_alert_timestamp"      : expiration_5m["expiration_alert_timestamp"],
        "status_alert"                    : status_alert,    
        "name_strategy"                   : name_strategy,
        "mercado"                         : mercado,
        "alert_time_update"               : expiration_5m["alert_time_update"],
    }
    if direction != "-":
        insert_database_M5(obj_msg_database)
    return obj_msg_database

    

def Strategy_1(list_dataframes, lista_dataframes_supp_res, padrao, status_alert, t_version):
    print(f"Processando Estratégia M5 - Versão 1 | Strategy_1")
    # print(list_dataframes)
    obj_sup_res = dict()
    list_name_actives = []
    list_name_timeframes = []
    
    for i in lista_dataframes_supp_res:
        print("*********************************** \n\n\n")
        name = list(i.keys())[0].split()[0]
        name_timeframe = list(i.keys())[0].split()[2]
        

        print(list(i.keys())[0], f"--> {name} | {name_timeframe}")
        name_obj = {list(i.keys())[0]: i[list(i.keys())[0]]}
        obj_sup_res.update(name_obj)

        if name not in list_name_actives:
            list_name_actives.append(name)
        
        if name_timeframe not in list_name_timeframes:
            list_name_timeframes.append(name_timeframe)
     
    
    for df in list_dataframes:
        request_id = df["active_name"][0].split()
        name_active = request_id[0]
        mercado = request_id[4]
        print("############################################ \n\n\n")
        print(request_id)
        print(name_active, mercado)
        # print(df)
        lista_df_res = []
        lista_df_sup = []
        #------
        lista_df_open = []
        lista_df_close = []

        # listas para resumo suporte e resistencia
        list_resume_touch_support = []
        list_resume_touch_resistence = []
        list_resume_touch_open = []
        list_resume_touch_close = []

        for idx in df.index:
            max_value       = float(df["max"][idx])
            min_value       = float(df["min"][idx])
            open_value      = float(df["open"][idx])
            close_value     = float(df["close"][idx])
            from_value      = df["from"][idx]
            active_name     = df["active_name"][idx]
            status_candle   = df["status_candle"][idx]
            
            # print(f"\n\nfrom: {from_value} | active: {active_name} | status: {status_candle} | open: {open_value} | max: {max_value} | min: {min_value} | close: {close_value}")
            
            # pavil
            list_support_touch = []
            list_resistence_touch = []

            # body
            list_open_touch = []
            list_close_touch = []

            for tmframe in list_name_timeframes:
                df_temp = obj_sup_res[f"{name_active} - {tmframe} - {mercado}"]

                for idx_df_temp in df_temp.index:
                    max_value_temp      = float(df_temp["max"][idx_df_temp])
                    min_value_temp      = float(df_temp["min"][idx_df_temp])

                    open_value_temp      = float(df_temp["open"][idx_df_temp])
                    close_value_temp      = float(df_temp["close"][idx_df_temp])

                    from_temp  = df_temp["from"][idx_df_temp]
                    active_name_temp  = df_temp["active_name"][idx_df_temp]
                    if from_value >= from_temp:
                        touch_candle = None
                        touch_candle_2 = None

                        if status_candle == "alta":
                            if max_value >= max_value_temp and close_value < max_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            elif max_value > max_value_temp and close_value <= max_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            elif max_value >= min_value_temp and close_value < min_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            elif max_value > min_value_temp and close_value <= min_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)

                            # --------------------------------
                            # -------------- support
                            # if min_value <= min_value_temp and open_value > min_value_temp:
                            #     touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_resistence_touch.append(touch_candle)
                            # elif min_value < min_value_temp and open_value >= min_value_temp:
                            #     touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_resistence_touch.append(touch_candle)

                            # # -------------- resistence
                            # elif max_value >= max_value_temp and close_value < max_value_temp:
                            #     touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_resistence_touch.append(touch_candle)
                            # elif max_value > max_value_temp and close_value <= max_value_temp:
                            #     touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_resistence_touch.append(touch_candle)

                            
                            
                            # # abertura
                            # if max_value > open_value_temp and close_value <= open_value_temp:
                            #     touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_open_touch.append(touch_candle_2)
                            # elif max_value >= open_value_temp and close_value < open_value_temp:
                            #     touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_open_touch.append(touch_candle_2)
                            
                            # # fechamento
                            # if max_value > close_value_temp and close_value <= close_value_temp:
                            #     touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_close_touch.append(touch_candle_2)
                            # elif max_value >= close_value_temp and close_value < close_value_temp:
                            #     touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_close_touch.append(touch_candle_2)
                        

                        # ----------------------------------------------------------------------------
                        elif status_candle == "baixa":
                            # --- suporte min
                            if min_value < min_value_temp and close_value >= min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            elif min_value <= min_value_temp and close_value > min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            # suporte min
                            elif min_value < max_value_temp and close_value >= max_value_temp:
                                touch_candle = f"{from_value} travou na resistência de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            elif min_value <= max_value_temp and close_value > max_value_temp:
                                touch_candle = f"{from_value} travou na resistência de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                         

                            #----------------------------
                            # --- resistence min
                            # if max_value >= max_value_temp and open_value < max_value_temp:
                            #     touch_candle = f"{from_value} travou na resistência de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_support_touch.append(touch_candle)
                            # elif max_value > max_value_temp and open_value <= max_value_temp:
                            #     touch_candle = f"{from_value} travou na resistência de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_support_touch.append(touch_candle)
                            # # ------
                            # elif max_value >= min_value_temp and open_value < min_value_temp:
                            #     touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_support_touch.append(touch_candle)
                            # elif max_value > min_value_temp and open_value <= min_value_temp:
                            #     touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_support_touch.append(touch_candle)


                            
                            # # abertura
                            # if min_value > open_value_temp and close_value <= open_value_temp:
                            #     touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                            #     list_open_touch.append(touch_candle_2)
                            # elif min_value >= open_value_temp and close_value < open_value_temp:
                            #     touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                            #     list_open_touch.append(touch_candle_2)
                            
                            # # fechamento
                            # if min_value > close_value_temp and close_value <= close_value_temp:
                            #     touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                            #     list_close_touch.append(touch_candle_2)
                            # elif min_value >= close_value_temp and close_value < close_value_temp:
                            #     touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                            #     list_close_touch.append(touch_candle_2)
                        

            # extrato detalhado de suportes e resistencias
            if len(list_resistence_touch) >= 1:
                lista_df_res.append(list_resistence_touch)
                list_resume_touch_resistence.append(len(list_resistence_touch))
            else:
                lista_df_res.append("-")
                list_resume_touch_resistence.append("-")
            # -------------------
            if len(list_support_touch) >= 1:
                lista_df_sup.append(list_resistence_touch)
                list_resume_touch_support.append(len(list_support_touch))
            else:
                lista_df_sup.append("-")
                list_resume_touch_support.append("-")
            # -------------------
            if len(list_open_touch) >= 1:
                lista_df_open.append(list_open_touch)
                list_resume_touch_open.append(len(list_open_touch))
            else:
                lista_df_open.append("-")
                list_resume_touch_open.append("-")
            # -------------------
            if len(list_close_touch) >= 1:
                lista_df_close.append(list_close_touch)
                list_resume_touch_close.append(len(list_close_touch))
            else:
                lista_df_close.append("-")
                list_resume_touch_close.append("-")

        df["resistence"]        = lista_df_res
        df["support"]           = lista_df_sup
        # --------
        df["resistence_open"]   = lista_df_open
        df["support_close"]     = lista_df_close
        # --------
        df["tt_resistence"]         = list_resume_touch_resistence
        df["tt_support"]            = list_resume_touch_support
        df["tt_resistence_open"]    = list_resume_touch_open
        df["tt_support_close"]      = list_resume_touch_close

        
        # ----- V1
        # direction_v1 = process_strategy_v1(df, name_active)
        # prepare_message_database(active=name_active, direction=direction_v1, resultado="process", padrao=f"{padrao}-V1", status_alert=status_alert, name_strategy=f"{name_active}-M5-V1", mercado=mercado, t_version="M5-V1")
        
        # ----- V2
        # direction_v2 = process_strategy_v2(df, name_active)
        # prepare_message_database(active=name_active, direction=direction_v2, resultado="process", padrao=f"{padrao}-V2", status_alert=status_alert, name_strategy=f"{name_active}-M5-V2", mercado=mercado, t_version="M5-V2")

        # ----- V4
        direction_v4 = process_strategy_v4(df, name_active)
        prepare_message_database(active=name_active, direction=direction_v4, resultado="process", padrao=f"{padrao}-V4", status_alert=status_alert, name_strategy=f"{name_active}-M5-V4", mercado=mercado, t_version="M5-V4")

# ------------------------------- alternativa para multiplo processamento
def process_strategy_v1(df, name_active):
    # validação de confluencia de suporter/resistencia e estratégia
    list_signs = []
    direction = "-"
    for current_id in df.index:
        try:
            
            id_7 = current_id -6
            id_6 = current_id -5
            id_5 = current_id -4
            id_4 = current_id -3
            id_3 = current_id -2
            id_2 = current_id -1
            id_1 = current_id -0

            if df["status_candle"][id_7] == "baixa" and df["status_candle"][id_6] == "alta" and df["status_candle"][id_5] == "alta" and df["status_candle"][id_4] == "baixa" and df["status_candle"][id_3] == "baixa" and df["status_candle"][id_2] == "alta":
                if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                    direction = "call"
                    list_signs.append(direction)
                else:
                    list_signs.append("call - sem confluencia")
                    
            elif df["status_candle"][id_7] == "alta" and df["status_candle"][id_6] == "baixa" and df["status_candle"][id_5] == "baixa" and df["status_candle"][id_4] == "alta" and df["status_candle"][id_3] == "alta" and df["status_candle"][id_2] == "baixa":
                if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                    direction = "put"
                    list_signs.append(direction)
                else:
                    list_signs.append("put - sem confluencia")
            else:
                list_signs.append("-")

        except Exception as e:
            print(e)
            list_signs.append("---")

    # --------
    df["signs"] = list_signs

    print(f"DataFrame ->> V1 - {name_active}")
    print(df)
    return direction

def process_strategy_v2(df, name_active):
    # validação de confluencia de suporter/resistencia e estratégia
    list_signs = []
    direction = "-"
    for current_id in df.index:
        try:
            
            id_7 = current_id -6
            id_6 = current_id -5
            id_5 = current_id -4
            id_4 = current_id -3
            id_3 = current_id -2
            id_2 = current_id -1
            id_1 = current_id -0

            if df["status_candle"][id_7] == "baixa" and df["status_candle"][id_6] == "alta" and df["status_candle"][id_5] == "baixa" and df["status_candle"][id_4] == "baixa" and df["status_candle"][id_3] == "baixa" and df["status_candle"][id_2] == "baixa":
                if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                    direction = "call"
                    list_signs.append(direction)
                else:
                    list_signs.append("call - sem confluencia")
                    
            elif df["status_candle"][id_7] == "alta" and df["status_candle"][id_6] == "baixa" and df["status_candle"][id_5] == "alta" and df["status_candle"][id_4] == "alta" and df["status_candle"][id_3] == "alta" and df["status_candle"][id_2] == "alta":
                if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                    direction = "put"
                    list_signs.append(direction)
                else:
                    list_signs.append("put - sem confluencia")
            else:
                list_signs.append("-")

        except Exception as e:
            print(e)
            list_signs.append("---")

    # --------
    df["signs"] = list_signs

    print(f"DataFrame ->> V2 - {name_active}")
    print(df)
    return direction

def process_strategy_v4(df, name_active):
    # validação de confluencia de suporter/resistencia e estratégia
    list_signs = []
    direction = "-"
    for current_id in df.index:
        try:
            
            id_7 = current_id -6
            id_6 = current_id -5
            id_5 = current_id -4
            id_4 = current_id -3
            id_3 = current_id -2
            id_2 = current_id -1
            id_1 = current_id -0


            tt_res      = df["tt_resistence"][id_1]
            tt_sup      = df["tt_support"][id_1]
            tt_open     = df["tt_resistence_open"][id_1]
            tt_close    = df["tt_support_close"][id_1]
            
            
            if df["status_candle"][id_7] == "baixa" and df["status_candle"][id_6] == "alta" and df["status_candle"][id_5] == "alta" and df["status_candle"][id_3] == "baixa":
                if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                    direction = "put"
                    list_signs.append(direction)
                    
                else:
                    list_signs.append("put - sem confluencia")
                    
            elif df["status_candle"][id_7] == "alta" and df["status_candle"][id_6] == "baixa" and df["status_candle"][id_5] == "baixa" and df["status_candle"][id_3] == "alta":
                if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                    direction = "call"
                    list_signs.append(direction)
                else:
                    list_signs.append("call - sem confluencia")
            else:
                list_signs.append("-")
                

        except Exception as e:
            print(e)
            list_signs.append("---")

    # --------
    df["signs"] = list_signs

    print(f"DataFrame ->> V4 - {name_active}")
    print(df)
    return direction


# ------------------------------- alternativa para processamento separado
def Strategy_2(list_dataframes, lista_dataframes_supp_res, padrao, status_alert, t_version):
    print(f"Processando Estratégia M5 - Versão 2 | Strategy_2")
    # print(list_dataframes)
    obj_sup_res = dict()
    list_name_actives = []
    list_name_timeframes = []
    
    for i in lista_dataframes_supp_res:
        print("*********************************** \n\n\n")
        name = list(i.keys())[0].split()[0]
        name_timeframe = list(i.keys())[0].split()[2]
        

        print(list(i.keys())[0], f"--> {name} | {name_timeframe}")
        name_obj = {list(i.keys())[0]: i[list(i.keys())[0]]}
        obj_sup_res.update(name_obj)

        if name not in list_name_actives:
            list_name_actives.append(name)
        
        if name_timeframe not in list_name_timeframes:
            list_name_timeframes.append(name_timeframe)
     
    
    for df in list_dataframes:
        request_id = df["active_name"][0].split()
        name_active = request_id[0]
        mercado = request_id[4]
        print("############################################ \n\n\n")
        print(request_id)
        print(name_active, mercado)
        # print(df)
        lista_df_res = []
        lista_df_sup = []
        #------
        lista_df_open = []
        lista_df_close = []

        # listas para resumo suporte e resistencia
        list_resume_touch_support = []
        list_resume_touch_resistence = []
        list_resume_touch_open = []
        list_resume_touch_close = []

        for idx in df.index:
            max_value       = float(df["max"][idx])
            min_value       = float(df["min"][idx])
            open_value      = float(df["open"][idx])
            close_value     = float(df["close"][idx])
            from_value      = df["from"][idx]
            active_name     = df["active_name"][idx]
            status_candle   = df["status_candle"][idx]
            
            # print(f"\n\nfrom: {from_value} | active: {active_name} | status: {status_candle} | open: {open_value} | max: {max_value} | min: {min_value} | close: {close_value}")
            
            # pavil
            list_support_touch = []
            list_resistence_touch = []

            # body
            list_open_touch = []
            list_close_touch = []

            for tmframe in list_name_timeframes:
                df_temp = obj_sup_res[f"{name_active} - {tmframe} - {mercado}"]

                for idx_df_temp in df_temp.index:
                    max_value_temp      = float(df_temp["max"][idx_df_temp])
                    min_value_temp      = float(df_temp["min"][idx_df_temp])

                    open_value_temp      = float(df_temp["open"][idx_df_temp])
                    close_value_temp      = float(df_temp["close"][idx_df_temp])

                    from_temp  = df_temp["from"][idx_df_temp]
                    active_name_temp  = df_temp["active_name"][idx_df_temp]
                    if from_value >= from_temp:
                        touch_candle = None
                        touch_candle_2 = None

                        if status_candle == "alta":
                            if max_value > max_value_temp and close_value <= max_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            elif max_value >= max_value_temp and close_value < max_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            
                            # abertura
                            if max_value > open_value_temp and close_value <= open_value_temp:
                                touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_open_touch.append(touch_candle_2)
                            elif max_value >= open_value_temp and close_value < open_value_temp:
                                touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_open_touch.append(touch_candle_2)
                            
                            # fechamento
                            if max_value > close_value_temp and close_value <= close_value_temp:
                                touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_close_touch.append(touch_candle_2)
                            elif max_value >= close_value_temp and close_value < close_value_temp:
                                touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_close_touch.append(touch_candle_2)
                        

                        # ----------------------------------------------------------------------------
                        elif status_candle == "baixa":
                            if min_value > min_value_temp and close_value <= min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            elif min_value >= min_value_temp and close_value < min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            
                            # abertura
                            if min_value > open_value_temp and close_value <= open_value_temp:
                                touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                                list_open_touch.append(touch_candle_2)
                            elif min_value >= open_value_temp and close_value < open_value_temp:
                                touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                                list_open_touch.append(touch_candle_2)
                            
                            # fechamento
                            if min_value > close_value_temp and close_value <= close_value_temp:
                                touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                                list_close_touch.append(touch_candle_2)
                            elif min_value >= close_value_temp and close_value < close_value_temp:
                                touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                                list_close_touch.append(touch_candle_2)
                        

            # extrato detalhado de suportes e resistencias
            if len(list_resistence_touch) >= 1:
                lista_df_res.append(list_resistence_touch)
                list_resume_touch_resistence.append(len(list_resistence_touch))
            else:
                lista_df_res.append("-")
                list_resume_touch_resistence.append("-")
            # -------------------
            if len(list_support_touch) >= 1:
                lista_df_sup.append(list_resistence_touch)
                list_resume_touch_support.append(len(list_support_touch))
            else:
                lista_df_sup.append("-")
                list_resume_touch_support.append("-")
            # -------------------
            if len(list_open_touch) >= 1:
                lista_df_open.append(list_open_touch)
                list_resume_touch_open.append(len(list_open_touch))
            else:
                lista_df_open.append("-")
                list_resume_touch_open.append("-")
            # -------------------
            if len(list_close_touch) >= 1:
                lista_df_close.append(list_close_touch)
                list_resume_touch_close.append(len(list_close_touch))
            else:
                lista_df_close.append("-")
                list_resume_touch_close.append("-")

        df["resistence"]        = lista_df_res
        df["support"]           = lista_df_sup
        # --------
        df["resistence_open"]   = lista_df_open
        df["support_close"]     = lista_df_close
        # --------
        df["tt_resistence"]         = list_resume_touch_resistence
        df["tt_support"]            = list_resume_touch_support
        df["tt_resistence_open"]    = list_resume_touch_open
        df["tt_support_close"]      = list_resume_touch_close

        
        # validação de confluencia de suporter/resistencia e estratégia
        list_signs = []
        direction = "-"
        # for current_id in df.index:
        #     try:
                
        #         id_7 = current_id -6
        #         id_6 = current_id -5
        #         id_5 = current_id -4
        #         id_4 = current_id -3
        #         id_3 = current_id -2
        #         id_2 = current_id -1
        #         id_1 = current_id -0

        #         if df["status_candle"][id_7] == "baixa" and df["status_candle"][id_6] == "alta" and df["status_candle"][id_5] == "baixa" and df["status_candle"][id_4] == "baixa" and df["status_candle"][id_3] == "baixa" and df["status_candle"][id_2] == "baixa":
        #             if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
        #                 direction = "call"
        #                 list_signs.append(direction)
        #             else:
        #                 list_signs.append("call - sem confluencia")
                     
        #         elif df["status_candle"][id_7] == "alta" and df["status_candle"][id_6] == "baixa" and df["status_candle"][id_5] == "alta" and df["status_candle"][id_4] == "alta" and df["status_candle"][id_3] == "alta" and df["status_candle"][id_2] == "alta":
        #             if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
        #                 direction = "put"
        #                 list_signs.append(direction)
        #             else:
        #                 list_signs.append("put - sem confluencia")
        #         else:
        #             list_signs.append("-")

        #     except Exception as e:
        #         print(e)
        #         list_signs.append("---")

        # # --------
        # df["signs"] = list_signs

        # print(f"DataFrame ->> V2 - {name_active}")
        # print(df)
        
        msg_db = prepare_message_database(
            active=name_active,
            direction=direction,
            resultado="process",
            padrao=padrao,
            status_alert=status_alert,
            name_strategy=f"{name_active}-{t_version}",
            mercado=mercado,
            t_version=t_version,
        )
        print(msg_db)

def Strategy_3(list_dataframes, lista_dataframes_supp_res, padrao, status_alert, t_version):
    
    print(f"Processando Estratégia M5 - Versão 3 | Strategy_3")
    # print(list_dataframes)
    obj_sup_res = dict()
    list_name_actives = []
    list_name_timeframes = []
    
    for i in lista_dataframes_supp_res:
        print("*********************************** \n\n\n")
        name = list(i.keys())[0].split()[0]
        name_timeframe = list(i.keys())[0].split()[2]
        

        print(list(i.keys())[0], f"--> {name} | {name_timeframe}")
        name_obj = {list(i.keys())[0]: i[list(i.keys())[0]]}
        obj_sup_res.update(name_obj)

        if name not in list_name_actives:
            list_name_actives.append(name)
        
        if name_timeframe not in list_name_timeframes:
            list_name_timeframes.append(name_timeframe)
     
    
    for df in list_dataframes:
        request_id = df["active_name"][0].split()
        name_active = request_id[0]
        mercado = request_id[4]
        print("############################################ \n\n\n")
        print(request_id)
        print(name_active, mercado)
        # print(df)
        lista_df_res = []
        lista_df_sup = []
        #------
        lista_df_open = []
        lista_df_close = []

        # listas para resumo suporte e resistencia
        list_resume_touch_support = []
        list_resume_touch_resistence = []
        list_resume_touch_open = []
        list_resume_touch_close = []

        for idx in df.index:
            max_value       = float(df["max"][idx])
            min_value       = float(df["min"][idx])
            open_value      = float(df["open"][idx])
            close_value     = float(df["close"][idx])
            from_value      = df["from"][idx]
            active_name     = df["active_name"][idx]
            status_candle   = df["status_candle"][idx]
            
            # print(f"\n\nfrom: {from_value} | active: {active_name} | status: {status_candle} | open: {open_value} | max: {max_value} | min: {min_value} | close: {close_value}")
            
            # pavil
            list_support_touch = []
            list_resistence_touch = []

            # body
            list_open_touch = []
            list_close_touch = []

            for tmframe in list_name_timeframes:
                df_temp = obj_sup_res[f"{name_active} - {tmframe} - {mercado}"]

                for idx_df_temp in df_temp.index:
                    max_value_temp      = float(df_temp["max"][idx_df_temp])
                    min_value_temp      = float(df_temp["min"][idx_df_temp])

                    open_value_temp      = float(df_temp["open"][idx_df_temp])
                    close_value_temp      = float(df_temp["close"][idx_df_temp])

                    from_temp  = df_temp["from"][idx_df_temp]
                    active_name_temp  = df_temp["active_name"][idx_df_temp]
                    if from_value >= from_temp:
                        touch_candle = None
                        touch_candle_2 = None

                        if status_candle == "alta":
                            if max_value >= max_value_temp and close_value < max_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            elif max_value > max_value_temp and close_value <= max_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            elif max_value >= min_value_temp and close_value < min_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            elif max_value > min_value_temp and close_value <= min_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)

                            # --------------------------------
                            # -------------- support
                            if min_value <= min_value_temp and open_value > min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            elif min_value < min_value_temp and open_value >= min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            # ---
                            elif min_value <= max_value_temp and open_value > max_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            elif min_value < max_value_temp and open_value >= max_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)

                            
                            
                            # # abertura
                            # if max_value > open_value_temp and close_value <= open_value_temp:
                            #     touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_open_touch.append(touch_candle_2)
                            # elif max_value >= open_value_temp and close_value < open_value_temp:
                            #     touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_open_touch.append(touch_candle_2)
                            
                            # # fechamento
                            # if max_value > close_value_temp and close_value <= close_value_temp:
                            #     touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_close_touch.append(touch_candle_2)
                            # elif max_value >= close_value_temp and close_value < close_value_temp:
                            #     touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                            #     list_close_touch.append(touch_candle_2)
                        

                        # ----------------------------------------------------------------------------
                        elif status_candle == "baixa":
                            # --- suporte min
                            if min_value < min_value_temp and close_value >= min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            elif min_value <= min_value_temp and close_value > min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            # suporte min
                            elif min_value < max_value_temp and close_value >= max_value_temp:
                                touch_candle = f"{from_value} travou na resistência de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            elif min_value <= max_value_temp and close_value > max_value_temp:
                                touch_candle = f"{from_value} travou na resistência de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                         

                            #----------------------------
                            # --- resistence min
                            if max_value >= max_value_temp and open_value < max_value_temp:
                                touch_candle = f"{from_value} travou na resistência de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            elif max_value > max_value_temp and open_value <= max_value_temp:
                                touch_candle = f"{from_value} travou na resistência de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            # ------
                            elif max_value >= min_value_temp and open_value < min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            elif max_value > min_value_temp and open_value <= min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)


                            
                            # # abertura
                            # if min_value > open_value_temp and close_value <= open_value_temp:
                            #     touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                            #     list_open_touch.append(touch_candle_2)
                            # elif min_value >= open_value_temp and close_value < open_value_temp:
                            #     touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                            #     list_open_touch.append(touch_candle_2)
                            
                            # # fechamento
                            # if min_value > close_value_temp and close_value <= close_value_temp:
                            #     touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                            #     list_close_touch.append(touch_candle_2)
                            # elif min_value >= close_value_temp and close_value < close_value_temp:
                            #     touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                            #     list_close_touch.append(touch_candle_2)
                        

            # extrato detalhado de suportes e resistencias
            if len(list_resistence_touch) >= 1:
                lista_df_res.append(list_resistence_touch)
                list_resume_touch_resistence.append(len(list_resistence_touch))
            else:
                lista_df_res.append("-")
                list_resume_touch_resistence.append("-")
            # -------------------
            if len(list_support_touch) >= 1:
                lista_df_sup.append(list_resistence_touch)
                list_resume_touch_support.append(len(list_support_touch))
            else:
                lista_df_sup.append("-")
                list_resume_touch_support.append("-")
            # -------------------
            if len(list_open_touch) >= 1:
                lista_df_open.append(list_open_touch)
                list_resume_touch_open.append(len(list_open_touch))
            else:
                lista_df_open.append("-")
                list_resume_touch_open.append("-")
            # -------------------
            if len(list_close_touch) >= 1:
                lista_df_close.append(list_close_touch)
                list_resume_touch_close.append(len(list_close_touch))
            else:
                lista_df_close.append("-")
                list_resume_touch_close.append("-")

        df["resistence"]        = lista_df_res
        df["support"]           = lista_df_sup
        # --------
        df["resistence_open"]   = lista_df_open
        df["support_close"]     = lista_df_close
        # --------
        df["tt_resistence"]         = list_resume_touch_resistence
        df["tt_support"]            = list_resume_touch_support
        df["tt_resistence_open"]    = list_resume_touch_open
        df["tt_support_close"]      = list_resume_touch_close

        
        # validação de confluencia de suporter/resistencia e estratégia
        list_signs = []
        direction = "-"
        for current_id in df.index:
            try:
                id_3 = current_id -2
                id_2 = current_id -1
                id_1 = current_id -0
                tt_res      = df["tt_resistence"][id_1]
                tt_sup      = df["tt_support"][id_1]
                tt_open     = df["tt_resistence_open"][id_1]
                tt_close    = df["tt_support_close"][id_1]

                if df["status_candle"][id_3] == "alta" and df["status_candle"][id_2] == "baixa" and df["status_candle"][id_1] == "baixa":
                    if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                        direction = "call"
                        list_signs.append(direction)
                    else:
                        list_signs.append("call - sem confluencia")
                      

                elif df["status_candle"][id_3] == "baixa" and df["status_candle"][id_2] == "alta" and df["status_candle"][id_1] == "alta":
                    if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                        direction = "put"
                        list_signs.append(direction)
                    else:
                        list_signs.append("put - sem confluencia")
                else:
                    list_signs.append("-")

            except Exception as e:
                print(e)
                list_signs.append("---")

        # --------
        df["signs"] = list_signs

        print(f"DataFrame ->> V3 - {name_active}")
        print(df)
        
        msg_db = prepare_message_database(
            active=name_active,
            direction=direction,
            resultado="process",
            padrao=padrao,
            status_alert=status_alert,
            name_strategy=f"{name_active}-{t_version}",
            mercado=mercado, 
            t_version=t_version,
        )
        print(msg_db)
    # validação de confluencia de suporter/resistencia e estratégia
        list_signs = []
        direction = "-"
        for current_id in df.index:
            try:
                
                id_7 = current_id -6
                id_6 = current_id -5
                id_5 = current_id -4
                id_4 = current_id -3
                id_3 = current_id -2
                id_2 = current_id -1
                id_1 = current_id -0


                tt_res      = df["tt_resistence"][id_1]
                tt_sup      = df["tt_support"][id_1]
                tt_open     = df["tt_resistence_open"][id_1]
                tt_close    = df["tt_support_close"][id_1]
              
                
                if df["status_candle"][id_7] == "baixa" and df["status_candle"][id_6] == "alta" and df["status_candle"][id_5] == "alta" and df["status_candle"][id_3] == "baixa":
                    if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                        direction = "put"
                        list_signs.append(direction)
                        
                    else:
                        list_signs.append("put - sem confluencia")
                        
                elif df["status_candle"][id_7] == "alta" and df["status_candle"][id_6] == "baixa" and df["status_candle"][id_5] == "baixa" and df["status_candle"][id_3] == "alta":
                    if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                        direction = "call"
                        list_signs.append(direction)
                    else:
                        list_signs.append("call - sem confluencia")
                else:
                    list_signs.append("-")
                   

            except Exception as e:
                print(e)
                list_signs.append("---")

        # --------
        df["signs"] = list_signs
    return direction

def Strategy_4(list_dataframes, lista_dataframes_supp_res, padrao, status_alert, t_version):

    print(f"Processando Estratégia M5 - Versão 4 | Strategy_3")
    # print(list_dataframes)
    obj_sup_res = dict()
    list_name_actives = []
    list_name_timeframes = []
    
    for i in lista_dataframes_supp_res:
        print("*********************************** \n\n\n")
        name = list(i.keys())[0].split()[0]
        name_timeframe = list(i.keys())[0].split()[2]
        


        # print(list(i.keys())[0], f"--> {name} | {name_timeframe}")
        name_obj = {list(i.keys())[0]: i[list(i.keys())[0]]}
        obj_sup_res.update(name_obj)

        if name not in list_name_actives:
            list_name_actives.append(name)
        
        if name_timeframe not in list_name_timeframes:
            list_name_timeframes.append(name_timeframe)

    
    
    for df in list_dataframes:
        request_id = df["active_name"][0].split()
        name_active = request_id[0]
        mercado = request_id[4]

        print("############################################ \n\n\n")
        print(request_id)
        print(name_active, mercado)
        # print(df)
        lista_df_res = []
        lista_df_sup = []
        #------
        lista_df_open = []
        lista_df_close = []

        # listas para resumo suporte e resistencia
        list_resume_touch_support = []
        list_resume_touch_resistence = []
        list_resume_touch_open = []
        list_resume_touch_close = []

        for idx in df.index:
            max_value       = float(df["max"][idx])
            min_value       = float(df["min"][idx])
            open_value      = float(df["open"][idx])
            close_value     = float(df["close"][idx])
            from_value      = df["from"][idx]
            active_name     = df["active_name"][idx]
            status_candle   = df["status_candle"][idx]
            
            # print(f"\n\nfrom: {from_value} | active: {active_name} | status: {status_candle} | open: {open_value} | max: {max_value} | min: {min_value} | close: {close_value}")
            
            # pavil
            list_support_touch = []
            list_resistence_touch = []

            # body
            list_open_touch = []
            list_close_touch = []

            for tmframe in list_name_timeframes:
                
                df_temp = obj_sup_res[f"{name_active} - {tmframe} - {mercado}"]

                for idx_df_temp in df_temp.index:
                    max_value_temp      = float(df_temp["max"][idx_df_temp])
                    min_value_temp      = float(df_temp["min"][idx_df_temp])

                    open_value_temp      = float(df_temp["open"][idx_df_temp])
                    close_value_temp      = float(df_temp["close"][idx_df_temp])

                    from_temp  = df_temp["from"][idx_df_temp]
                    active_name_temp  = df_temp["active_name"][idx_df_temp]
                    if from_value >= from_temp:
                        touch_candle = None
                        touch_candle_2 = None
                    
                        if status_candle == "alta":
                            if max_value > max_value_temp and close_value <= max_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            elif max_value >= max_value_temp and close_value < max_value_temp:
                                touch_candle = f"{from_value} travou na resistencia de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_resistence_touch.append(touch_candle)
                            
                            # abertura
                            if max_value > open_value_temp and close_value <= open_value_temp:
                                touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_open_touch.append(touch_candle_2)
                            elif max_value >= open_value_temp and close_value < open_value_temp:
                                touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_open_touch.append(touch_candle_2)
                            
                            # fechamento
                            if max_value > close_value_temp and close_value <= close_value_temp:
                                touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_close_touch.append(touch_candle_2)
                            elif max_value >= close_value_temp and close_value < close_value_temp:
                                touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_close_touch.append(touch_candle_2)
                        


                        # ----------------------------------------------------------------------------
                        elif status_candle == "baixa":
                            if min_value > min_value_temp and close_value <= min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            elif min_value >= min_value_temp and close_value < min_value_temp:
                                touch_candle = f"{from_value} travou no suporte de {from_temp} - {active_name_temp} | max: {max_value_temp} | min: {min_value_temp}"
                                list_support_touch.append(touch_candle)
                            
                            # abertura
                            if min_value > open_value_temp and close_value <= open_value_temp:
                                touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                                list_open_touch.append(touch_candle_2)
                            elif min_value >= open_value_temp and close_value < open_value_temp:
                                touch_candle_2 = f"{from_value} travou na abertura de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                                list_open_touch.append(touch_candle_2)
                            
                            # fechamento
                            if min_value > close_value_temp and close_value <= close_value_temp:
                                touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                                list_close_touch.append(touch_candle_2)
                            elif min_value >= close_value_temp and close_value < close_value_temp:
                                touch_candle_2 = f"{from_value} travou no fechamento de {from_temp} - {active_name_temp} | open: {open_value_temp} | close: {close_value_temp}"
                                list_close_touch.append(touch_candle_2)
                        
                        # print(f"---------------->>> idx_df_temp: {idx_df_temp} | {tmframe} | {touch_candle}")
            # print(list_resistence_touch)
            # print(list_support_touch)
            # print(f"Total resistence: {len(list_resistence_touch)}")
            # print(f"Total support: {len(list_support_touch)}")

            # # print(list_open_touch)
            # # print(list_close_touch)
            # print(f"Total open: {len(list_open_touch)}")
            # print(f"Total close: {len(list_close_touch)}")

            # extrato detalhado de suportes e resistencias
            if len(list_resistence_touch) >= 1:
                lista_df_res.append(list_resistence_touch)
                list_resume_touch_resistence.append(len(list_resistence_touch))
            else:
                lista_df_res.append("-")
                list_resume_touch_resistence.append("-")
            # -------------------
            if len(list_support_touch) >= 1:
                lista_df_sup.append(list_resistence_touch)
                list_resume_touch_support.append(len(list_support_touch))
            else:
                lista_df_sup.append("-")
                list_resume_touch_support.append("-")
            # -------------------
            if len(list_open_touch) >= 1:
                lista_df_open.append(list_open_touch)
                list_resume_touch_open.append(len(list_open_touch))
            else:
                lista_df_open.append("-")
                list_resume_touch_open.append("-")
            # -------------------
            if len(list_close_touch) >= 1:
                lista_df_close.append(list_close_touch)
                list_resume_touch_close.append(len(list_close_touch))
            else:
                lista_df_close.append("-")
                list_resume_touch_close.append("-")

        df["resistence"]        = lista_df_res
        df["support"]           = lista_df_sup
        # --------
        df["resistence_open"]   = lista_df_open
        df["support_close"]     = lista_df_close
        # --------
        df["tt_resistence"]         = list_resume_touch_resistence
        df["tt_support"]            = list_resume_touch_support
        df["tt_resistence_open"]    = list_resume_touch_open
        df["tt_support_close"]      = list_resume_touch_close

        


        # validação de confluencia de suporter/resistencia e estratégia
        list_signs = []
        direction = "-"
        for current_id in df.index:
            try:
                
                id_7 = current_id -6
                id_6 = current_id -5
                id_5 = current_id -4
                id_4 = current_id -3
                id_3 = current_id -2
                id_2 = current_id -1
                id_1 = current_id -0


                tt_res      = df["tt_resistence"][id_1]
                tt_sup      = df["tt_support"][id_1]
                tt_open     = df["tt_resistence_open"][id_1]
                tt_close    = df["tt_support_close"][id_1]
              
                
                if df["status_candle"][id_7] == "baixa" and df["status_candle"][id_6] == "alta" and df["status_candle"][id_5] == "alta" and df["status_candle"][id_3] == "baixa":
                    if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                        direction = "put"
                        list_signs.append(direction)
                        
                    else:
                        list_signs.append("put - sem confluencia")
                        
                elif df["status_candle"][id_7] == "alta" and df["status_candle"][id_6] == "baixa" and df["status_candle"][id_5] == "baixa" and df["status_candle"][id_3] == "alta":
                    if df["support"][id_1] != "-" or df["resistence"][id_1] != "-" or df["resistence_open"][id_1] != "-" or df["support_close"][id_1] != "-":
                        direction = "call"
                        list_signs.append(direction)
                    else:
                        list_signs.append("call - sem confluencia")
                else:
                    list_signs.append("-")
                   

            except Exception as e:
                print(e)
                list_signs.append("---")

        # --------
        df["signs"] = list_signs
        # df["result"] = lista_result
        # df["detailed_result"] = list_detailed_result



        # df.to_excel(f"base/strategy_4/V4 - {name_active}.xlsx")
        print(f"DataFrame ->> V4 - {name_active}")
        print(df)
        
        msg_db = prepare_message_database(
            active=name_active,
            direction=direction,
            resultado="process",
            padrao=padrao,
            status_alert=status_alert,
            name_strategy=f"{name_active}-{t_version}",
            mercado=mercado,
            t_version=t_version, 
        )
        print(msg_db)
    
        

