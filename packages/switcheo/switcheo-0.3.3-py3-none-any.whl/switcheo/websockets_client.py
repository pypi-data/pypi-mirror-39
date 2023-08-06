import json
import time
from websocket import create_connection, WebSocketConnectionClosedException
from threading import Thread


class WebsocketsClient(object):
    def __init__(self,
                 url='wss://test-ws.switcheo.io',
                 products=None,
                 message_type="subscribe",
                 should_print=True,
                 auth=False,
                 api_key="",
                 api_secret="",
                 api_passphrase="",
                 channels=None):
        self.url = url
        self.products = products
        self.channels = channels
        self.type = message_type
        self.stop = True
        self.error = None
        self.ws = None
        self.thread = None
        self.keep_alive = None
        self.message_count = 0
        self.auth = auth
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.should_print = should_print

    def start(self):
        def _go():
            self._connect()
            self._listen()
            self._disconnect()

        self.stop = False
        self.on_open()
        self.thread = Thread(target=_go)
        self.keep_alive = Thread(target=self._keepalive)
        self.thread.start()

    def _connect(self):
        if self.products is None:
            self.products = ["SWTH_NEO"]
        elif not isinstance(self.products, list):
            self.products = [self.products]

        if self.url[-1] == "/":
            self.url = self.url[:-1]

        if self.channels is None:
            # sub_params = {'type': 'subscribe', 'product_ids': self.products}
            sub_params = {
                "blockchain": "neo",
                "contractHash": "91b83e96f2a7c4fdf0c1688441ec61986c7cae26",
                "pair": "SWTH_NEO"
            }
        else:
            # sub_params = {'type': 'subscribe', 'product_ids': self.products, 'channels': self.channels}
            sub_params = {
                "blockchain": "neo",
                "contractHash": "91b83e96f2a7c4fdf0c1688441ec61986c7cae26",
                "pair": "SWTH_NEO"
            }

        # if self.auth:
            # timestamp = str(time.time())
            # message = timestamp + 'GET' + '/users/self/verify'
            # auth_headers = get_auth_headers(timestamp, message, self.api_key, self.api_secret, self.api_passphrase)
            # sub_params['signature'] = auth_headers['CB-ACCESS-SIGN']
            # sub_params['key'] = auth_headers['CB-ACCESS-KEY']
            # sub_params['passphrase'] = auth_headers['CB-ACCESS-PASSPHRASE']
            # sub_params['timestamp'] = auth_headers['CB-ACCESS-TIMESTAMP']

        self.ws = create_connection(self.url)

        self.ws.send(json.dumps(sub_params))

    def _keepalive(self, interval=30):
        while self.ws.connected:
            self.ws.ping("keepalive")
            time.sleep(interval)

    def _listen(self):
        self.keep_alive.start()
        while not self.stop:
            try:
                data = self.ws.recv()
                msg = json.loads(data)
            except ValueError as e:
                self.on_error(e)
            except Exception as e:
                self.on_error(e)
            else:
                self.on_message(msg)

    def _disconnect(self):
        try:
            if self.ws:
                self.ws.close()
        except WebSocketConnectionClosedException as e:
            print(e)
            pass
        finally:
            self.keep_alive.join()

        self.on_close()

    def close(self):
        self.stop = True    # will only disconnect after next msg recv
        self._disconnect()  # force disconnect so threads can join
        self.thread.join()

    def on_open(self):
        if self.should_print:
            print("-- Subscribed! --\n")

    def on_close(self):
        if self.should_print:
            print("\n-- Socket Closed --")

    def on_message(self, msg):
        if self.should_print:
            print(msg)

    def on_error(self, e, data=None):
        self.error = e
        self.stop = True
        print('{} - data: {}'.format(e, data))


# if __name__ == "__main__":
#     import sys
#     import time
#
    #
    # class MyWebsocketClient(ws.WebsocketsClient):
    #     def on_open(self):
    #         self.url = 'wss://test-ws.switcheo.io'
    #         self.products = ['SWTH_NEO']
    #         self.message_count = 0
    #         print("Let's count the messages!")
    #
    #     def on_message(self, msg):
    #         print(json.dumps(msg, indent=4, sort_keys=True))
    #         self.message_count += 1
    #
    #     def on_close(self):
    #         print("-- Goodbye! --")

    # wsClient = MyWebsocketClient()
    # wsClient.start()
    # print(wsClient.url, wsClient.products)
    # try:
    #     while True:
    #         print("\nMessageCount =", "%i \n" % wsClient.message_count)
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     wsClient.close()

    # if wsClient.error:
    #     sys.exit(1)
    # else:
    #     sys.exit(0)


from socketIO_client_nexus import SocketIO, BaseNamespace, LoggingNamespace
import logging

logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

class BooksNamespace(BaseNamespace):

   def on_event(self, event, *args):
       print('on_response', event, args)

   def on_connect(self):
       logging.info('connected')

   def on_disconnect(self):
       logging.info('disconnect')

class TradesNamespace(BaseNamespace):

   def on_event(self, event, *args):
       print('on_response', event, args)

   def on_connect(self):
       logging.info('connected')

   def on_disconnect(self):
       logging.info('disconnect')



url = 'https://ws.switcheo.io'
joinDict = {"blockchain":"neo","contractHash":"91b83e96f2a7c4fdf0c1688441ec61986c7cae26","pair":"SWTH_NEO"}


socketIO = SocketIO(url, None, LoggingNamespace, transports="websocket", verify=True )
#, cert=('client.crt', 'client.key'))

books  = socketIO.define(BooksNamespace, '/v2/books')
trades = socketIO.define(TradesNamespace, '/v2/books')
books.emit("join", joinDict)
trades.emit("join",joinDict)

socketIO.wait()
