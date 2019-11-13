import gzip
import json

import websocket


def on_message(ws, message):
    # if isinstance(message, bytes):
    #     message = gzip.decompress(message).decode("utf-8")
    # message = json.loads(message)
    # print(message)
    # if isinstance(message, dict):
    #     if 'ping' in message:
    #         pong = {'pong': message['ping']}
    #         ws.send(json.dumps(pong))
    print(message)

def on_error(ws, error):
    print('!!! error !!!', error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print('opened')
    data = {"sub": {'category': 0, 'star': []}}
    # data = {"sub": {'category': 1, 'star': ['ETH']}}
    # data = {"sub": {'category': 2, 'star': ['BTC/USDT.huobi']}}
    # data = {"unsub": {'category': 2, 'star': ['BTC/USDT.huobi']}}
    ws.send(json.dumps(data))


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000/v1/ws/marketpair",
                                on_message=on_message,
                                on_open=on_open,
                                on_error=on_error,
                                on_close=on_close)
    # ws.on_open = on_open
    ws.run_forever()
