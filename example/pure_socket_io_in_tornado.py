from abc import ABC
import time

import socketio
import asyncio
import tornado.websocket
import tornado.ioloop
from tornado.web import Application

sio = socketio.AsyncServer(async_mode='tornado', cors_allowed_origins="*")


@sio.on('connect')
def connect(sid, data):
    print(sid, ' connected!')
    print('data: ', data)
    return sid


@sio.on('hello')
def hello(sid):
    print(sid, ' said hello!')
    return 'world'


@sio.on('get_json')
def get_json(sid):
    time.sleep(1.234)
    return {'tth': [2, 3, 4], 'azi': [5, 6, 7], 'q': None, 'd': [10, 11, 12]}


class WebSocketHandler(tornado.websocket.WebSocketHandler, ABC):
    def open(self, *args):
        print("New connection")
        self.write_message("Welcome!")

    def on_message(self, message):
        print("New message {}".format(message))
        self.write_message(message.upper())

    def on_close(self):
        print("Connection closed")


def make_app():
    return tornado.web.Application(
        [
            (r"/socket.io/", socketio.get_tornado_handler(sio)),
            (r"/ws/", WebSocketHandler),
        ],
    )


def start_server(port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start_server(9458)
