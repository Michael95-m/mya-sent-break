from fastapi import FastAPI, UploadFile, Query, Form
from utils import sent_break_syl
from normalize.normalize_data import Normalization
from typing import Union
from pydantic import BaseModel

app = FastAPI()

norm_obj = Normalization()
sent_break_obj = sent_break_syl('data_syl')

class Text_data(BaseModel):
    text: str
    show_log: Union[bool, None] = None

@app.get("/")
async def hello():

    return {"text": "hello"}

@app.post("/segment_sent")
async def segment_sent(text_data: Text_data):

    segment_text = sent_break_obj.break_sent(text_data.text, text_data.show_log)

    return {"segment_text": segment_text}

@app.post("/segment_file")
async def segment_file(text_file: UploadFile, show_log: Union[bool, None] = Form(default=False)):

    raw_txt = text_file.file.read()
    text = raw_txt.decode()
    print(f"show_log param is {show_log}")
    segment_text = sent_break_obj.break_sent(text, show_log)

    return {"segment_text": segment_text}


