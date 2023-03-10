import pandas as pd
from strategy.controllers.convert_data.convert_datetime import convert_timestamp_to_datetime

def convert_json_to_dataframe(obj_data, active_name):
    df_temp = pd.DataFrame(obj_data)
    list_col_active_name = list(map(lambda x: active_name, range(len(df_temp))))
    # print(list_col_active_name)
    
    list_status_candle = []
    
    for id in df_temp.index:
        # print(id)
        if df_temp["close"][id] > df_temp["open"][id]:
            list_status_candle.append("alta")
        elif df_temp["close"][id] < df_temp["open"][id]:
            list_status_candle.append("baixa")
        else:
            list_status_candle.append("sem mov.")

        timestamp = df_temp["from"][id]
        df_temp["from"][id] = convert_timestamp_to_datetime(
            timestamp=timestamp, local_tz="UTC", local="America/Sao_Paulo")

    df_temp["active_name"]   = list_col_active_name
    df_temp["status_candle"] = list_status_candle

    df_temp[["open", "close", "min", "max"]] = df_temp[["open", "close", "min", "max"]].astype(float, errors="raise")
    df_temp["from"] = pd.to_datetime(df_temp["from"], format="%Y/%m/%d %H:%M:%S")
    
    # df_temp.to_excel(f"base/{active_name}.xlsx")

    return df_temp

def convert_json_to_dataframe_sup_res(obj_data, active_name):
    df_temp = pd.DataFrame(obj_data)
    list_col_active_name = list(map(lambda x: active_name, range(len(df_temp))))
    # print(list_col_active_name)
    
    list_status_candle = []
    
    for id in df_temp.index:
        # print(id)
        if df_temp["close"][id] > df_temp["open"][id]:
            list_status_candle.append("alta")
        elif df_temp["close"][id] < df_temp["open"][id]:
            list_status_candle.append("baixa")
        else:
            list_status_candle.append("sem mov.")

        timestamp = df_temp["from"][id]
        df_temp["from"][id] = convert_timestamp_to_datetime(
            timestamp=timestamp, local_tz="UTC", local="America/Sao_Paulo")

    df_temp["active_name"]   = list_col_active_name
    df_temp["status_candle"] = list_status_candle

    df_temp[["open", "close", "min", "max"]] = df_temp[["open", "close", "min", "max"]].astype(float, errors="raise")
    df_temp["from"] = pd.to_datetime(df_temp["from"], format="%Y/%m/%d %H:%M:%S")
    return {f"{active_name}": df_temp}