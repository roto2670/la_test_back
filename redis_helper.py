# -*- coding: utf-8 -*-
#
# Copyright 2019-2020 Naran Inc. All rights reserved.
#  __    _ _______ ______   _______ __    _
# |  |  | |   _   |    _ | |   _   |  |  | |
# |   |_| |  |_|  |   | || |  |_|  |   |_| |
# |       |       |   |_||_|       |       |
# |  _    |       |    __  |       |  _    |
# | | |   |   _   |   |  | |   _   | | |   |
# |_|  |__|__| |__|___|  |_|__| |__|_|  |__|


import json
import logging

import redis

from constants import REDIS_HOST, REDIS_PORT
from constants import PROFILE_REDIS_DB


class RedisStore(object):
  def __init__(self, host, port, db):
    self.store = redis.StrictRedis(host=host, port=port, db=db)

  def set_data(self, name, key, value):
    try:
      _ret = self.store.hset(name, key, json.dumps(value))
      return True if _ret else False
    except:
      logging.exception("Raise error while set data. key : %s, data : %s",
                        key, value)

  def has_data(self, name, key):
    ret = self.store.hexists(name, key)
    return True if ret else False

  def delete_data(self, name, key):
    ret = self.store.hdel(name, key)
    return True if ret else False

  def get_data(self, name, key):
    _ret = self.has_data(name, key)
    if _ret:
      _data = self.store.hget(name, key)
      if _data is None:
        return None
      return json.loads(_data)
    else:
      return None

  def get_all(self, name):
    datas = self.store.hgetall(name)
    ret = {k.decode("utf-8"): json.loads(v.decode("utf-8")) for k, v in datas.items()}
    return ret

# crate redis db
DATA = RedisStore(REDIS_HOST, REDIS_PORT, PROFILE_REDIS_DB)

# table name
__LOGIN_DATA__ = '''__LOGIN_DATA__'''
__TASK_DATA__ = '''__TASK_DATA__'''

# common
#def del_data(name):
#  DATA.clear_data(name)
#  return True


# login data block {{{
def set_join_data(key, value):
  ret = DATA.set_data(__LOGIN_DATA__, key, value)
  return ret


def get_join_data(key):
  ret = DATA.has_data(__LOGIN_DATA__, key)
  return ret

#}}}

# task data block {{{
def set_data(key, value):
  ret = DATA.set_data(__TASK_DATA__, key, value)
  return ret


def get_data(key):
  ret = DATA.get_data(__TASK_DATA__, key)
  return ret


def get_all_data():
  ret = DATA.get_all(__TASK_DATA__)
  return ret


def data_exist(key):
  data = DATA.get_data(__TASK_DATA__, key)
  ret = True if data else False
  return ret
# }}}