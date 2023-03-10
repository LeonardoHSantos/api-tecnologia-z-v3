import websocket
from strategy.controllers.convert_data.convert import ConvertData
from strategy.controllers.process_data.process_data_actives_open import process_open_actives

class WSS_Client:
    def __init__(self, url_wss):
        self.url_wss = url_wss
        self.status_conn = False
        self.status_msg = False

        self.list_requests = []
        self.obj_candles = dict()
        self.df_actives_open = None
        self.status_process_dataframe = False

        self.wss = websocket.WebSocketApp(
            url=url_wss,
            on_message=self.on_message,
            on_open=self.on_open,
            on_close=self.on_close,
        )
    
    def on_message(self, message):
        self.status_msg = True
        # print(f"Status MSG: {self.status_msg}")
        
        message = ConvertData.convert_to_json(data=message)
        # print(message)

        if message["name"] == "candles":
            name = message["request_id"]
            obj_request = {f"{name}": message}
            self.obj_candles.update(obj_request)

        elif message["name"] == "initialization-data":
            print(" ********************* Mensagem actives open ********************* ")
            self.df_actives_open = process_open_actives(message["msg"])
            self.status_process_dataframe = True


    
    def on_open(self):
        print("### Conexão aberta com Websocket ###")
        self.status_conn = True
        print(f"Status CONN: {self.status_conn}")

    def on_close(self):
        self.wss.close()
        self.status_conn = False
        self.status_msg = False
        print("### Conexão encerrada com Websocket ###")