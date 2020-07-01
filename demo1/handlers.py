# coding: utf-8

import tornado
from tornado.web import RequestHandler
from pycket.session import SessionMixin
from models import DBSession
from models import User


class BaseHandler(RequestHandler):
    def initialize(self):
        self.db = DBSession()
        #self.db.begin()

    def finished(self):
        #self.db.close()
        pass


class AuthHandler(BaseHandler, SessionMixin):

    def get_current_user(self):
        return self.session.get('userinfo', None)



class IndexHandler(AuthHandler):
    def get(self):
        #users = self.db.query(User)
        if self.current_user:
            #self.write(f'hello {self.current_user.username}')
            self.render('index.html', username=self.current_user.username)
        else:
            self.redirect("/login")
            #self.render('login.html')


class LoginHandler(AuthHandler):
    def get(self):
        if self.current_user:
            return self.redirect("/")
        else:
            self.render('login.html')

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        user = self.db.query(User).filter(User.username==username, User.password==password).one()
        #user = self.db.query(User).filter_by(**{
        #    "username":username,
        #    "password":password}).one()
        if user:
            self.session["userinfo"] = user
            self.redirect("/")
        else:
            self.redirect("/login")

class LogoutHandler(AuthHandler):
    def get(self):
        if self.current_user:
            del self.session["userinfo"]
        self.redirect("/")

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html", error="")

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        print("*"*100)
        print(username)
        print(password)
        confirm_password = self.get_argument('confirm_password', None)
        print(confirm_password)
        if confirm_password != password:
            return self.render("register.html", error="password confirm error")
        count = self.db.query(User).filter_by(**{"username":username}).count()
        print("xxxx count xxxx")
        print(count)
        if count > 0:
            return self.render("register.html", error="username exist!please input other")
        user = User()
        user.username = username
        user.password = password
        self.db.add(user)
        self.db.flush()
        self.db.commit()
        self.session["userinfo"] = user
        self.redirect("/")



handler_list = [
    (r"/", IndexHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/register", RegisterHandler),
]

