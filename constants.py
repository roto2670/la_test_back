import os

# backtool server
IS_DEV = True
SERVER_PORT = 4557

CHAR_SEARCH_URL = '''https://lostark.game.onstove.com/Profile/Character/'''


# REDIS
REDIS_HOST = '''127.0.0.1'''
REDIS_PORT = 6379
LOGIN_REDIS_DB = 1
TASK_REDIS_DB = 2
LOGIN_ACT_REDIS_DB = 3

TASK_DATA_FORM = {
    "201": False,
    "202": False,
    "203": False,
    "204": False,
    "301": False,
    "401": False,
    "501": False,
}


#encrypt / decrypt
IV = "aaaaaaaaaabbbbbb".encode('utf-8')
ENC_KEY = "aaaaaaaaaabbbbbb".encode('utf-8')

#response code
DATA_EXIST = '''data exist'''
JOIN_SUCCESS = '''join success'''
JOIN_FAIL = '''join fail'''

LOGIN_OK = '''login ok'''
NO_ID = '''no id'''
NO_PW = '''no pw'''