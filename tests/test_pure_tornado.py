from tornado.testing import AsyncHTTPSTestCase
from example.pure_tornado import make_app


class TestWorldHandler(AsyncHTTPSTestCase):
    def get_app(self):
        return make_app()

    def test_hello_world(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'Hello World')
