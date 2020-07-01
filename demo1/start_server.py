# coding: utf-8

import tornado
from tornado import ioloop
from tornado.web import RequestHandler
from tornado.options import options, define
from pycket.session import SessionMixin
from handlers import handler_list


define('port', default=8888, help='listening port', type=int)
options.parse_command_line()


class BaseHandler(RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('userinfo', None)


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("hello world")


class LoginHandler(RequestHandler):
    def get(self):
        self.write("hello world")


class MyApplication(tornado.web.Application):
    def __init__(self):
        #handlers = [
        #    (r"/", IndexHandler),
        #    (r"/login", LoginHandler),
        #]
        handlers = handler_list
        settings = dict(
            template_path = 'templates',
            login_url = '/login',
            cookie_secret = '123456',
            pycket = {
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                },
                'cookie': {
                    'expires_days': 1
                }
            },
            autoreload=True
        )
        super(MyApplication, self).__init__(handlers, **settings)

app = MyApplication()

if __name__ == '__main__':
    app.listen(options.port)
    print(f'app start at {options.port}')
    ioloop.IOLoop.current().start()
