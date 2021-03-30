import tornado.ioloop
from tornado.web import Application, url, RequestHandler
from abc import ABCMeta, ABC
import secrets


class BaseHandler(RequestHandler, ABC):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header("Access-Control-Allow-Headers", '*')
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Headers",
                        "Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, "
                        "Access-Control-Allow-Methods")

    def options(self):
        pass

    def get_user_id(self):
        if not self.get_secure_cookie("userid"):
            self.user_id += 1
            self.set_secure_cookie("userid", str(self.user_id), expires_days=None)
            self.sessions[self.user_id] = {}
            return self.user_id
        else:
            return self.get_secure_cookie("userid")


class MainHandler(BaseHandler, metaclass=ABCMeta):
    def get(self):
        self.write('Hello World')


def make_app():
    return Application([
        url(r"/", MainHandler),
    ], cookie_secret=secrets.token_bytes(16))


def start_server(port):
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start_server(9456)
