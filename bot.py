import websocket
import json
import config
from binance.client import Client
from binance.enums import *
import time
# socket source
# change 1m below to any timeframe you want ex: @kline_30m
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
# Symbol Pair to trade with
symbol = 'ETHUSDT'
# Enable Buy and Sell positions
buyPosition = True
sellPosition = True
tradeQuantity = 1
callBackRatio = 0.1
# configure client
# disable testnet=True if you want to trade with real account
client = Client(config.API_KEY, config.API_SECRET, testnet=True)


def on_open(ws):
    print("opened connection")


def on_close(ws):
    print("closed connection")


def on_message(ws, message):
    global client, buyPosition, sellPosition, symbol, tradeQuantity, callBackRatio
    json_message = json.loads(message)

    candle = json_message['k']
    openn = float(candle['o'])
    close = float(candle['c'])
    difference = openn-close
    if buyPosition:
        # difference between candle open price and current candle price:
        if difference >= 5:
            stop = close-10.0
            take = close+10
            print('Opened a BUY Position!')
            print("normal price is:", close)
            print("Stop price is:", stop)
            order = client.futures_create_order(
                symbol=symbol, side='BUY', type='TRAILING_STOP_MARKET', quantity=tradeQuantity, callBackRate=callBackRatio)
            # Sleep for 5 minutes once a trade is open
            time.sleep(300)

    if sellPosition:
        # difference between candle open price and current candle price:
        if difference <= -5:
            print('Opened a SELL Position!')
            stop = close+10
            take = close-10
            print("normal price is:", close)
            print("Stop price is:", stop)
            #clear = client.futures_cancel_all_open_orders(symbol='ETHUSDT')
            order = client.futures_create_order(
                symbol=symbol, side='SELL', type='TRAILING_STOP_MARKET', quantity=tradeQuantity, callBackRate=callBackRatio)
            # Sleep for 5 minutes once a trade is open
            time.sleep(300)


ws = websocket.WebSocketApp(
    SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
