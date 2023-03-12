from strategy.actives import PARIDADES, TIMEFRAMES_NAME
from strategy.controllers.prepare_data import prepare_data
import json

class ChannelsWSS:
    def ssid(**kwargs):
        name = "ssid"
        return prepare_data.prepare_msg(name=name, msg=kwargs["ssid"], request_id="")
    
    def get_candles(active_name, timeframe, expiration, amount, actives_open):
        name = 'sendMessage'
        mercado = actives_open[actives_open["ticker"]==active_name]["mercado"].values[0]

        message = {
            'name': 'get-candles',
            'version': '2.0',
            'body': {
                'active_id': PARIDADES[active_name],
                'size': timeframe,
                'to': expiration,
                'count': amount,
            }
        }
        request_id = f"{active_name} - {TIMEFRAMES_NAME[timeframe]} - {mercado}"
        print(f"\n\n\n\n ########### request_id: {request_id}")
        return prepare_data.prepare_msg(name=name, msg=message, request_id=request_id)
    
    def get_candles_alternative(active_name, timeframe, expiration, amount):
        name = 'sendMessage'
        
        message = {
            'name': 'get-candles',
            'version': '2.0',
            'body': {
                'active_id': PARIDADES[active_name],
                'size': timeframe,
                'to': expiration,
                'count': amount,
            }
        }
        request_id = f"{active_name} - {TIMEFRAMES_NAME[timeframe]}"
        print(f"\n\n\n\n ########### request_id: {request_id}")
        return prepare_data.prepare_msg(name=name, msg=message, request_id=request_id)
    

    def get_actives_open():

        name = 'sendMessage'
        message = {'name': 'get-initialization-data', 'version': '3.0', 'body': {}}
        request_id = 'get-underlying-list'
        return prepare_data.prepare_msg(name=name, msg=message, request_id=request_id)
    
        
        
     

        # name = "sendMessage"
        # message = {"name": "get-initialization-data", "version": "3.0", "body": {}}
        # request_id = "get-underlying-list"
        # return prepare_data.prepare_msg(name=name, msg=message, request_id=request_id)
