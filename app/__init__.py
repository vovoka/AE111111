
from config import Config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler(
    'logs/orders.log', maxBytes=10240, backupCount=20)
file_handler.setFormatter(logging.Formatter('%(asctime)s|%(message)s'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

csrf = CSRFProtect()
csrf.init_app(app)

from app import routes, errors
