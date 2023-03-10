from strategy import var_globals
from strategy.controllers.channels.channels import ssid

def send_message(content):
    return var_globals.OBJ_WSS.wss.send(content)






