import json
from fastapi import HTTPException
from langchain.callbacks import get_openai_callback
from topic_classification.predict import predict_topic
from retrieval import retrieve
from generate_answer import completion

def chat(prompt):
    try:
        with get_openai_callback() as cb:
            topic = predict_topic(prompt)
            information_relevant = retrieve(topic=topic, prompt=prompt)
            response = completion(information_relevant=information_relevant, prompt=prompt)
            if 'error' in topic:
                raise HTTPException(status_code=503)
            response_data = {
                "question" : prompt,
                "topic_predict": topic,
                "response":response
            }
            response_json = json.dumps(response_data, indent=4)
            return response_json
    except Exception as e:
        error_message = str(e)
        return json.dumps({'error': error_message}, indent=4)
