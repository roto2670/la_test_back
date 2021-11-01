from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from urllib.request import urlopen
import urllib.parse
import json
from bs4 import BeautifulSoup
from bs4.element import NavigableString


test_data = {
  1: "test data 1",
  2: {"test" : "test str"},
}
post_data = {}
app = FastAPI()
origins = ["*"]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


class Item(BaseModel):
  content: dict


@app.get("/get_test")
def get_test():
  return test_data


#테스트 코드 // 개인용
@app.get("/tt/{target_id}")
def get_test(target_id):
  ret = {}
  real_lv = None
  _target_id = urllib.parse.quote_plus(target_id)
  url = urlopen('https://lostark.game.onstove.com/Profile/Character/'+_target_id)
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
    #test block {{{

    #}}}
    ret['lv'] = real_lv
    ret['char_list'] = test_list
    return ret


if __name__ == "__main__":
  #run command = uvicorn main:app --reload --port=4557
  uvicorn.run(app, host='0.0.0.0', port=4557)


