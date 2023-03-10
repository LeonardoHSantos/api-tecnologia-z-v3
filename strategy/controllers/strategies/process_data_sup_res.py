import pandas as pd

def Check_sup_res(df, obj_sup_res):
    print(f"Processando Estratégia M5 - Versão 3 | Strategy_3")
    
    
    list_name_timeframes = []

    request_id = df["active_name"][0].split()
    name_active = request_id[0]
    print("############################################ \n\n\n")
    print(request_id)
    print(name_active)
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
        
        print(f"\n\nfrom: {from_value} | active: {active_name} | status: {status_candle} | open: {open_value} | max: {max_value} | min: {min_value} | close: {close_value}")
        
        # pavil
        list_support_touch = []
        list_resistence_touch = []

        # body
        list_open_touch = []
        list_close_touch = []

        for tmframe in list_name_timeframes:
            df_temp = obj_sup_res[f"{name_active} - {tmframe}"]

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
                    
                    print(f"---------------->>> idx_df_temp: {idx_df_temp} | {tmframe} | {touch_candle}")
        print(list_resistence_touch)
        print(list_support_touch)
        print(f"Total resistence: {len(list_resistence_touch)}")
        print(f"Total support: {len(list_support_touch)}")

        print(list_open_touch)
        print(list_close_touch)
        print(f"Total open: {len(list_open_touch)}")
        print(f"Total close: {len(list_close_touch)}")

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
    return df


