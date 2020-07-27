import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    # Load dotenv settings
    dotenv_path = os.path.join(basedir, '.env')
    load_dotenv(dotenv_path)

    # Load secrets from dotenv
    SHOP_ID = int(os.environ.get('SHOP_ID'))
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    SHOP_CURRENCY = int(os.environ.get('SHOP_CURRENCY'))


