"predict.py for intent classification"
import os
import warnings
import logging
import tensorflow as tf
from transformers import logging as tf_log
from transformers import TFBertForSequenceClassification, AutoTokenizer
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

tf_log.set_verbosity_error()
warnings.filterwarnings("ignore")
logging.getLogger("tensorflow").setLevel(logging.ERROR)

model = TFBertForSequenceClassification.from_pretrained("iqbalpurba26/IndoBERT-topic-classification")
tokenizer = AutoTokenizer.from_pretrained("iqbalpurba26/IndoBERT-topic-classification")
topics = ["alergi", "obat", "menstruasi"]

def predict_topic(prompt):
    """
    This function to classification topic of user's prompt

    Args:
    prompt : string, user prompt

    Return
    intents[pred_topic_id] : topic class
    """
    encodings = tokenizer(prompt, return_tensors="tf", padding=True, truncation=True, max_length=64)
    logits = model(encodings).logits
    probabilities = tf.nn.softmax(logits, axis=1).numpy()[0]
    pred_topic_id = tf.argmax(probabilities).numpy()
    confidence_pred = probabilities[pred_topic_id]

    return topics[pred_topic_id]


