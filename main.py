from html import entities
from typing import List
from fastapi import FastAPI, Form
from pydantic import BaseModel

import uvicorn
from ultil import on_success, on_fail, read_text_from_input_to_one
import flair
from flair.models import SequenceTagger

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
async def get_ner(obj_input: Input):
    # Đọc input đầu vào
    try:
        print('Oke1')
        sentences = obj_input.sentences
        result = []
        print('Oke2')
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
                # text = entity.text
                # ner_tag = entity.get_label("ner").value
                # print(f'entity.text is: "{entity.text}"')s
                # print(f'entity.tag is: "{ner_tag}"')
                # print(f'entity.start_position is: "{entity.start_position}"')
                # print(f'entity.end_position is: "{entity.end_position}"')
                entities.append(entity)
            obj['entities'] = entities
            result.append(obj)
        print(result)
        print('OKe3')
        return on_success(result)
    except Exception as err:
        print(err)
        on_fail()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
