from tornado import testing, websocket
from example.pure_socket_io_in_tornado import make_app


class TestWSHandler(testing.AsyncHTTPTestCase):
    def setUp(self) -> None:
        super(TestWSHandler, self).setUp()
        self.ws_url = "ws://localhost:" + str(self.get_http_port()) + "/ws"

    def get_app(self):
        return make_app()

    @testing.gen_test
    def test_handshake(self):
        ws_client = yield websocket.websocket_connect(self.ws_url)
        response = yield ws_client.read_message()
        self.assertEqual('hello', response)

    @testing.gen_test
    def test_message_response(self):
        ws_client = yield websocket.websocket_connect(self.ws_url)
        _ = yield ws_client.read_message()  # discard handshake

        ws_client.write_message("elephants are small")
        response = yield ws_client.read_message()
        self.assertEqual("ELEPHANTS ARE SMALL", response)
