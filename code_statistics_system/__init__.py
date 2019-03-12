# -*-coding:utf-8-*-
# @author: JinFeng
# @date: 2019/3/8 15:21

from flask import Flask
from .views.account import account
from .views.statistics import ind
from settings import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(account)
    app.register_blueprint(ind)

    return app


