import os

#Config Section
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REGISTERED_USERS = {}