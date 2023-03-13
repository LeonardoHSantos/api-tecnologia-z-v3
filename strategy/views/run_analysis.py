import threading
import pandas as pd
from time import sleep
from datetime import datetime, timedelta

from strategy.actives import PARIDADES


from strategy.controllers.auth.auth import auth
from strategy.models.wss.client import WSS_Client

from strategy.var_globals import URL_HTTP, URL_WSS, OBJ_WSS
from strategy.var_data_aux import LIST_MINUTES_STRATEGY_V1, LIST_MINUTES_STRATEGY_V1_10S, LIST_MINUTES_STRATEGY_V1_CHECK_RESULTS
from strategy.var_data_aux import LIST_MINUTES_STRATEGY_V2, LIST_MINUTES_STRATEGY_V2_10S
from strategy.var_data_aux import LIST_MINUTES_STRATEGY_V3, LIST_MINUTES_STRATEGY_V3_10S, LIST_MINUTES_STRATEGY_V3_CHECK_RESULTS
from strategy.var_data_aux import LIST_MINUTES_STRATEGY_V4, LIST_MINUTES_STRATEGY_V4_10S


from strategy.controllers.channels.channels import ChannelsWSS

from strategy.controllers.convert_data.convert_datetime import expiration_datetime
from strategy.controllers.convert_data.convert_to_dataframe import convert_json_to_dataframe, convert_json_to_dataframe_sup_res

from strategy.controllers.strategies.strategies import Strategy_1, Strategy_2, Strategy_3, Strategy_4

from strategy.controllers.strategies.check_results import update_results_database



class RunAnalysys:
    def __init__(self, identifier, password):
        self.identifier = identifier
        self.password = password
        self.threading = None
        self.obj_wss = None
        self.actives_open = None
    
    def auth_broker(self):
        auth_user = auth(identifier=self.identifier, password=self.password, url_http=URL_HTTP)
        return auth_user
    
    def close_connection_wss(self):
        self.obj_wss.wss.close()
    
    def connect_wss(self):
        ssid = self.auth_broker()
        msg_ssid = ChannelsWSS.ssid(ssid=ssid["ssid"])
        self.obj_wss = WSS_Client(url_wss=URL_WSS)
        self.threading = threading.Thread(target=self.obj_wss.wss.run_forever).start()
        while True:
            if self.obj_wss.status_conn == True and self.obj_wss.status_msg == True:
                break
        self.obj_wss.wss.send(msg_ssid)
        print(f"Mensagem enviada SSID: {msg_ssid}")

    def get_actives_open(self):
        sleep(2)
        msg_actives_open = ChannelsWSS.get_actives_open()
        self.obj_wss.wss.send(msg_actives_open)
        print(f"Mensagem get candles open: {msg_actives_open}")
        while True:
            try:
                if len(self.obj_wss.df_actives_open) >= 0:
                    break
            except:
                pass
        actives_open = self.obj_wss.df_actives_open
        self.obj_wss.df_actives_open = None
        return actives_open
    
    def get_candles(self, list_active_name, timeframe, amount, tzone, list_support_resistence, amount_sup):
        actives_open = self.get_actives_open()
        list_active_name = actives_open["ticker"].values
        

        expiration = expiration_datetime(tzone=tzone)["exp_timestamp"]
        total_list_requests = 0
        for active_name in list_active_name:
            if active_name in PARIDADES.keys():
                msg_get_candles = ChannelsWSS.get_candles(active_name, timeframe, expiration, amount, actives_open)
                self.obj_wss.list_requests.append(msg_get_candles)
                self.obj_wss.wss.send(msg_get_candles)
                total_list_requests += 1
                print(f">>> MSG GET CANDLE ENVIADA: {msg_get_candles}")
        
        while True:
            if len(self.obj_wss.obj_candles) == len(self.obj_wss.list_requests):
                break
        
        print(f" -------- processo get_candles finalizando -------- ") #: {self.obj_wss.obj_candles}")
        lista_dataframes = self.convert_lists_to_dataframe(obj_candles=self.obj_wss.obj_candles)
        self.obj_wss.list_requests.clear()
        self.obj_wss.obj_candles.clear()

        lista_dataframes_sup_res = self.get_candles_sup_res(
            list_active_name=list_active_name, 
            timeframe=timeframe, 
            amount_sup=amount_sup, 
            tzone=tzone, 
            list_support_resistence=list_support_resistence,
            actives_open=actives_open,
        )
        # self.close_connection_wss()
        return {"lista_dataframes": lista_dataframes, "lista_dataframes_sup_res":lista_dataframes_sup_res}
    
    def get_candles_sup_res(self, list_active_name, timeframe, tzone, list_support_resistence, amount_sup, actives_open):

        expiration = expiration_datetime(tzone=tzone)["exp_timestamp"]
        total_list_requests = 0
        for active_name in list_active_name:
            for tm_frame in list_support_resistence:
                msg_get_candles = ChannelsWSS.get_candles(active_name, tm_frame, expiration, amount_sup, actives_open)
                self.obj_wss.list_requests.append(msg_get_candles)
                self.obj_wss.wss.send(msg_get_candles)
                total_list_requests += 1
                print(f">>> MSG GET CANDLES SUP/RES ENVIADA: {msg_get_candles}")
        
        while True:
            if len(self.obj_wss.obj_candles) == len(self.obj_wss.list_requests):
                break
        
        print(f" ------ processo get_candles SUP/RES finalizando ------ ") #: {self.obj_wss.obj_candles}")
        lista_dataframes_sup_res = self.convert_lists_to_dataframe_sup_res(obj_candles=self.obj_wss.obj_candles)
        self.obj_wss.list_requests.clear()
        self.obj_wss.obj_candles.clear()

        # self.close_connection_wss()
        return {"lista_dataframes_sup_res": lista_dataframes_sup_res}

    def get_candles_check_result(self, list_active_name, timeframe, amount, tzone):
        actives_open = self.get_actives_open()
        list_active_name = actives_open["ticker"].values
        
        expiration = expiration_datetime(tzone=tzone)["exp_timestamp"]
        total_list_requests = 0
        for active_name in list_active_name:
            if active_name in PARIDADES.keys():
                msg_get_candles = ChannelsWSS.get_candles(active_name, timeframe, expiration, amount, actives_open)
                self.obj_wss.list_requests.append(msg_get_candles)
                self.obj_wss.wss.send(msg_get_candles)
                total_list_requests += 1
                print(f">>> MSG GET CANDLES CHECK-RESULT ENVIADA: {msg_get_candles}")
        
        while True:
            if len(self.obj_wss.obj_candles) == len(self.obj_wss.list_requests):
                break
        
        print(f" -------- processo get_candles finalizando -------- ") #: {self.obj_wss.obj_candles}")
        lista_dataframes = self.convert_lists_to_dataframe(obj_candles=self.obj_wss.obj_candles)
        self.obj_wss.list_requests.clear()
        self.obj_wss.obj_candles.clear()

        return lista_dataframes

    def get_candles_alternative(self, active_name, timeframe, amount, tzone, tt_loop):
        sleep(2)
        # expiration = expiration_datetime(tzone=tzone)["exp_timestamp"]
        lista_df = []
        try:
            
            for i in range(tt_loop):
                expiration = expiration = datetime.now() - timedelta(minutes=i*1000)
                expiration = int(expiration.timestamp())

                print(f" ********** expiration: {expiration}")
                msg_get_candles = ChannelsWSS.get_candles_alternative(active_name, timeframe, expiration, amount)
                self.obj_wss.list_requests.append(msg_get_candles)
                self.obj_wss.wss.send(msg_get_candles)

                print(f">>> MSG GET CANDLE ALTERNATIVE ENVIADA: {msg_get_candles}")
                    
                while True:
                    if len(self.obj_wss.obj_candles) == len(self.obj_wss.list_requests):
                        break
                
                print(f" -------- processo get_candles finalizando -------- ") #: {self.obj_wss.obj_candles}")
                dataframe = self.convert_lists_to_dataframe(obj_candles=self.obj_wss.obj_candles)
                lista_df.append(dataframe)
                self.obj_wss.list_requests.clear()
                self.obj_wss.obj_candles.clear()

            
            self.close_connection_wss()
            return lista_df
        except Exception as e:
            print(f"Erro: {e}")
            return lista_df  

    def get_candles_check_alternative(self, list_active_name, timeframe, amount, tzone, list_support_resistence, amount_sup):
        base = self.get_candles(list_active_name, timeframe, amount, tzone, list_support_resistence, amount_sup)
        candles = base["lista_dataframes"]
        for df in candles:
            name = df["active_name"][0]
            df.to_excel(f"base/teste/{name}.xlsx")

    def convert_lists_to_dataframe(self, obj_candles):
        print(f"Process: convert_lists_to_dataframe")
        lista_dataframes = []
        for key in obj_candles.keys():
            print(f"--------->>> {key}")
            data = obj_candles[key]["msg"]["candles"]
            lista_dataframes.append(convert_json_to_dataframe(obj_data=data, active_name=key))
        return lista_dataframes
    
    def convert_lists_to_dataframe_sup_res(self, obj_candles):
        print(f"Process: convert_lists_to_dataframe")
        lista_dataframes = []
        for key in obj_candles.keys():
            # print(f"--------->>> {key}")
            data = obj_candles[key]["msg"]["candles"]
            lista_dataframes.append(convert_json_to_dataframe_sup_res(obj_data=data, active_name=key))
        return lista_dataframes

    # -------------------------------------- check result strategies
    def check_result_strategies(self, lista_padroes):
        actives_open = self.get_actives_open()
        list_active_name = actives_open["ticker"].values
        data_inicio = datetime.now()

        timeframe = 60*5
        tzone = "America/Sao_Paulo"
        amount = 2
        lista_dataframes = self.get_candles_check_result(list_active_name, timeframe, amount, tzone)
        update_results_database(obj_database=lista_dataframes, lista_padroes=lista_padroes)

    # -------------------------------------- strategies
    
    def strategy_1(self, status_alert, t_version, padrao):
        actives_open = self.get_actives_open()
        list_active_name = actives_open["ticker"].values
        data_inicio = datetime.now()

        timeframe = 60*5
        tzone = "America/Sao_Paulo"
        amount = 7
        amount_sup = 15
        list_support_resistence = [60*15, 60*60, 60*(60*4)]
        candles_v3 = self.get_candles(list_active_name, timeframe, amount, tzone, list_support_resistence, amount_sup)
        list_dataframes = candles_v3["lista_dataframes"]
        lista_dataframes_supp_res = candles_v3["lista_dataframes_sup_res"]["lista_dataframes_sup_res"]
        Strategy_1(list_dataframes=list_dataframes,
                   lista_dataframes_supp_res=lista_dataframes_supp_res,
                   status_alert=status_alert,
                   t_version=t_version,
                   padrao=padrao,
                   )
        data_fim = datetime.now()
        print(f"\n\n ------------------------------------------------ V1 - Tempo tt process: {data_fim - data_inicio}")

    def strategy_2(self, status_alert, t_version, padrao):
        actives_open = self.get_actives_open()
        list_active_name = actives_open["ticker"].values
        data_inicio = datetime.now()
        timeframe = 60*5
        tzone = "America/Sao_Paulo"
        amount = 7
        amount_sup = 15
        list_support_resistence = [60*15, 60*60, 60*(60*4)]
        candles_v3 = self.get_candles(list_active_name, timeframe, amount, tzone, list_support_resistence, amount_sup)
        list_dataframes = candles_v3["lista_dataframes"]
        lista_dataframes_supp_res = candles_v3["lista_dataframes_sup_res"]["lista_dataframes_sup_res"]
        Strategy_2(list_dataframes=list_dataframes,
                   lista_dataframes_supp_res=lista_dataframes_supp_res,
                   status_alert=status_alert,
                   t_version=t_version,
                   padrao=padrao,
                   )
        data_fim = datetime.now()
        print(f"\n\n ------------------------------------------------ V2 - Tempo tt process: {data_fim - data_inicio}")
    
    def strategy_3(self, status_alert, t_version, padrao):
        data_inicio = datetime.now()
        actives_open = self.get_actives_open()
        list_active_name = actives_open["ticker"].values

        timeframe = 60*5
        tzone = "America/Sao_Paulo"
        amount = 3
        amount_sup = 15
        list_support_resistence = [60*15, 60*60, 60*(60*4)]
        candles_v3 = self.get_candles(list_active_name, timeframe, amount, tzone, list_support_resistence, amount_sup)
        list_dataframes = candles_v3["lista_dataframes"]
        lista_dataframes_supp_res = candles_v3["lista_dataframes_sup_res"]["lista_dataframes_sup_res"]
        Strategy_3(list_dataframes=list_dataframes,
                   lista_dataframes_supp_res=lista_dataframes_supp_res,
                   status_alert=status_alert,
                   t_version=t_version,
                   padrao=padrao,
                   )
        data_fim = datetime.now()
        print(f"\n\n ------------------------------------------------ V3 - Tempo tt process: {data_fim - data_inicio}")
    
    def strategy_4(self, status_alert, t_version, padrao):
        actives_open = self.get_actives_open()
        list_active_name = actives_open["ticker"].values
        data_inicio = datetime.now()

        timeframe = 60*5
        tzone = "America/Sao_Paulo"
        amount = 7
        amount_sup = 15
        list_support_resistence = [60*15, 60*60, 60*(60*4)]
        candles_v4 = self.get_candles(list_active_name, timeframe, amount, tzone, list_support_resistence, amount_sup)
        list_dataframes = candles_v4["lista_dataframes"]
        lista_dataframes_supp_res = candles_v4["lista_dataframes_sup_res"]["lista_dataframes_sup_res"]

        Strategy_4(
            list_dataframes=list_dataframes,
            lista_dataframes_supp_res=lista_dataframes_supp_res,
            status_alert=status_alert,
            t_version=t_version,
            padrao=padrao
            )
        data_fim = datetime.now()
        print(f"\n\n ------------------------------------------------ V4 - Tempo tt process: {data_fim - data_inicio}")
    
    
    
    def initiate_strategies(self):
        while True:
            try:
                date = datetime.now()
                minutes = date.minute
                seconds = date.second
                # compartilhando 1, 2 e 4
                
                # check results
                if minutes in LIST_MINUTES_STRATEGY_V1_CHECK_RESULTS and seconds >= 3 and seconds <= 4:
                    lista_padroes = ["V1", "V2", "V4"]
                    self.check_result_strategies(lista_padroes=lista_padroes)
                # if minutes in LIST_MINUTES_STRATEGY_V3_CHECK_RESULTS and seconds >= 3 and seconds <= 4:
                #     lista_padroes = ["V3"]
                #     self.check_result_strategies(lista_padroes=lista_padroes)


                # ----------------------------------------------------------------------- versão 1, 2 e 4
                if minutes in LIST_MINUTES_STRATEGY_V1.keys():
                    status_alert = None
                    
                    if seconds >= 25 and seconds <= 26 and minutes in LIST_MINUTES_STRATEGY_V1_10S.keys():
                        status_alert = LIST_MINUTES_STRATEGY_V1_10S[minutes]

                    elif seconds >= 14 and seconds <= 15:
                        status_alert = LIST_MINUTES_STRATEGY_V1[minutes]
                    
                    if status_alert != None:
                        self.strategy_1(status_alert=status_alert, t_version="M5-V1", padrao="PADRAO-M5")
                
                # ----------------------------------------------------------------------- versão 3
                if minutes in LIST_MINUTES_STRATEGY_V3.keys():
                    status_alert = None
                    
                    if seconds >= 40 and seconds <= 41 and minutes in LIST_MINUTES_STRATEGY_V3_10S.keys():
                        status_alert = LIST_MINUTES_STRATEGY_V3_10S[minutes]

                    elif seconds >= 14 and seconds <= 15:
                        status_alert = LIST_MINUTES_STRATEGY_V3[minutes]
                    
                    if status_alert != None:
                        pass
                        # self.strategy_3(status_alert=status_alert, t_version="M5-V3", padrao="PADRAO-M5-V3")

                
                # ----------------------------------------------------------------------- versão 2
                # if minutes in LIST_MINUTES_STRATEGY_V2.keys():
                #     status_alert = None
                    
                #     if seconds >= 35 and seconds <= 36 and minutes in LIST_MINUTES_STRATEGY_V2_10S.keys():
                #         status_alert = LIST_MINUTES_STRATEGY_V2_10S[minutes]

                #     elif seconds >= 18 and seconds <= 19:
                #         status_alert = LIST_MINUTES_STRATEGY_V2[minutes]
                    
                #     if status_alert != None:
                #         self.strategy_2(status_alert=status_alert, t_version="M5-V2", padrao="PADRAO-M5-V2")

                # # ----------------------------------------------------------------------- versão 4
                # if minutes in LIST_MINUTES_STRATEGY_V4.keys():
                #     status_alert = None
                
                #     if seconds >= 42 and seconds <= 43 and minutes in LIST_MINUTES_STRATEGY_V4_10S.keys():
                #         status_alert = LIST_MINUTES_STRATEGY_V4_10S[minutes]

                #     elif seconds >= 25 and seconds <= 26:
                #         status_alert = LIST_MINUTES_STRATEGY_V4[minutes]
                    
                #     if status_alert != None:
                #         self.strategy_4(status_alert=status_alert, t_version="M5-V4", padrao="PADRAO-M5-V4")
            except Exception as e:
                print(f"Erro com o processamento da API: {e}")

    