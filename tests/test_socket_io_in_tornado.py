import tornado
import tornado.ioloop
import asyncio
import time
import threading
import unittest
from example.pure_socket_io_in_tornado import start_server

import socketio


class SocketIOServer(unittest.TestCase):
    port = 65231

    @classmethod
    def setUpClass(cls) -> None:
        cls.server_thread = threading.Thread(target=start_server,
                                             args=(cls.port,),
                                             daemon=True)
        cls.server_thread.start()

    def setUp(self):
        self.client = socketio.Client()
        self.client.connect("http://localhost:" + str(self.port))

    def tearDown(self) -> None:
        self.client.disconnect()

    def _callback(self, res):
        self.callback_result = res
        self.callback_called = True

    def emit(self, message: str) -> object:
        self.callback_called = False
        self.callback_result = None

        self.client.emit(message, callback=self._callback)
        while not self.callback_called:
            time.sleep(0.01)
        return self.callback_result

    def test_hello_world(self):
        self.assertEqual(self.emit('hello'), 'world')

    def test_multiple_args(self):
        res = self.emit('get_json')
        self.assertIn('tth', res.keys())
