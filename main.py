import json
from fastapi import FastAPI, HTTPException
from query_input import QueryInput
from chat import chat
from tools.validation import validate_prompt

app = FastAPI()

@app.post("/chatbot")
def get_response(query_input:QueryInput):
    text = query_input.prompt
    text = validate_prompt(text)
    try:
        res = chat(text)
        res_final = json.loads(res)
        return res_final
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))