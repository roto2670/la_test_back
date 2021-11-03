from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from constants import SERVER_PORT
import api_func
import redis_helper


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


#@app.get("/charname")
#def get_char_data():
  #get_all_data = redis_helper.get_all_data()
  #print("get_all_data : ", get_all_data)
  #return None


@app.get("/chardata/{target_id}")
def get_char_data(target_id):
  ret = api_func.search_char_data(target_id)
  return ret


@app.post("/taskdata")
def put_test(pul_data: Item):
  req_data = pul_data.content
  redis_helper.set_data(req_data['char_name'], req_data['task'])
  return True


if __name__ == "__main__":
  #run command = uvicorn main:app --reload --port=4557
  uvicorn.run(app, host='0.0.0.0', port=SERVER_PORT)


