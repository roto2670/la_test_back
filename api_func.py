from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4.element import NavigableString
import urllib.parse
import json

from constants import CHAR_SEARCH_URL, TASK_DATA_FORM, DATA_EXIST, JOIN_SUCCESS
from constants import JOIN_FAIL, LOGIN_OK, NO_ID, NO_PW
import redis_helper


def set_task_data(task_data):
  login_id = task_data['login_id']
  char_name = task_data['char_name']
  task = task_data['task']
  ret = redis_helper.set_task_data(login_id, char_name, task)
  return ret


def _chk_data_exist(login_id, char_id):
  data_exist = redis_helper.data_exist(login_id, char_id)
  return data_exist


def search_char_data(login_id, char_id):
  ret = {}
  real_lv = None
  task_data = {}
  _target_id = urllib.parse.quote_plus(char_id)
  url = urlopen(CHAR_SEARCH_URL +_target_id)
  page_data = BeautifulSoup(url, "html.parser")
  attention = page_data.main.find("div", {"class": "profile-attention"})
  if attention:
    return json.dumps(None)

  else:
    lv_tag = page_data.main.find("div", {"class": "level-info2__expedition"}).find_all("span")
    lv = lv_tag[-1]

    for con in lv:
      if isinstance(con, NavigableString):
        real_lv = con
    real_lv = str(real_lv).replace(",", "")
    char_list = page_data.main.find("div", {"id": "expand-character-list"}).find_all("button")
    test_list = []

    for _char_con in char_list:
      char_url = _char_con.get('onclick')
      if isinstance(char_url, str):
        char_name = char_url.split('/')[-1]
        char_name = char_name[:-1]
        test_list.append(char_name)

    data_exist = _chk_data_exist(login_id, char_id)
    if data_exist:
      task_data = redis_helper.get_task_data(login_id, char_id)
    else:
      task_data = TASK_DATA_FORM
      redis_helper.set_task_data(login_id, char_id, task_data)

    ret['lv'] = real_lv
    ret['char_list'] = test_list
    ret['task_data'] = task_data
    return ret


def join_user(join_data):
  _id = join_data['id']
  ret = redis_helper.set_join_data(_id, join_data)
  return ret


def check_user(_id):
  ret = redis_helper.get_join_data(_id)
  return ret


def join_account(join_data):
  data_exist = check_user(join_data['id'])
  if data_exist:
    ret = DATA_EXIST
  else:
    join_result = join_user(join_data)
    if join_result:
      ret = JOIN_SUCCESS
    else:
      ret = JOIN_FAIL
  return ret


def login_user(login_data):
  exist_data = redis_helper.get_login_data(login_data['id'])
  if exist_data:
    if exist_data['pw'] == login_data['pw']:
      ret = LOGIN_OK
    else:
      ret = NO_PW
  else:
    ret = NO_ID
  return ret