from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4.element import NavigableString
import urllib.parse
import json

from constants import CHAR_SEARCH_URL, TASK_DATA_FORM
import redis_helper


def set_task_data(task_data):
  ret = redis_helper.set_data(task_data['char_name'], task_data['task'])
  return ret


def _chk_data_exist(target_id):
  data_exist = redis_helper.data_exist(target_id)
  return data_exist


def search_char_data(target_id):
  ret = {}
  real_lv = None
  task_data = {}
  _target_id = urllib.parse.quote_plus(target_id)
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

    data_exist = _chk_data_exist(target_id)
    if data_exist:
      task_data = redis_helper.get_data(target_id)
    else:
      task_data = TASK_DATA_FORM
      redis_helper.set_data(target_id, task_data)

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