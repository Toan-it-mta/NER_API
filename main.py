from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from ultil import on_success, on_fail, read_text_from_input_to_one
import flair
from flair.models import SequenceTagger
import os
import json

app = FastAPI()
model = SequenceTagger.load('./model/best-model.pt')


class Sentence(BaseModel):
    text: str


class Input(BaseModel):
    sentences: List[Sentence]

class Output:
    def __init__(self, result):
        self.reuslt = result


@app.post('/ner')
def get_ner(obj_input: Input):
    # Đọc input đầu vào
    try:
        sentences = obj_input.sentences
        result = []
        for sentence in sentences:
            input_sentence = flair.data.Sentence(sentence.text)
            model.predict(input_sentence)
            obj = {}
            obj['text'] = sentence.text
            entities = []
            for ner in input_sentence.get_spans('ner'):
                entity = {}
                entity['text'] = ner.text
                entity['tag'] = ner.get_label("ner").value
                entity['start_position'] = ner.start_position
                entity['end_position'] = ner.end_position
                entities.append(entity)
            obj['entities'] = entities
            result.append(obj)
        return on_success(result)
    except Exception as err:
        return on_fail(err)




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # get_File('06_2019_NQ-HDTP_414764_tokened')