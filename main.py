from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from constants import SERVER_PORT, IV, ENC_KEY
import api_func
import redis_helper

# legacy import blco {{{
from Crypto.Cipher import AES
import base64
# }}}

# FAST API config {{{
app = FastAPI()
origins = ["*"]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
# }}}}

class Item(BaseModel):
  content: dict


@app.get("/charname")
def get_char_data():
  get_all_data = redis_helper.get_all_data()
  return get_all_data


@app.get("/chardata/{target_id}")
def get_char_data(target_id):
  ret = api_func.search_char_data(target_id)
  return ret


@app.post("/taskdata")
def set_task_data(post_data: Item):
  task_data = post_data.content
  ret = api_func.set_task_data(task_data)
  return ret


@app.post("/join")
def join_account(post_data: Item):
  join_data = post_data.content
  ret = api_func.join_account(join_data)
  return ret


@app.post("/login")
def login(post_data: Item):
  login_data = post_data.content
  ret = api_func.login_user(login_data)
  return ret


# legacy def block {{{

# def decrypt(encrypted):
#   aes = AES.new(ENC_KEY, AES.MODE_CBC, IV)
#   return aes.decrypt(base64.b64decode(encrypted))

#}}}

if __name__ == "__main__":
  #run command = uvicorn main:app --reload --port=4557
  uvicorn.run(app, host='0.0.0.0', port=SERVER_PORT)


