# -*- coding: utf-8 -*-
"""Salinan_dari_FINE_TUNING_FROM_SCRATCH.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1J_mmW19IQJ39UP1UBVYeowp-JSvsRD4m
"""

!pip install transformers tensorflow pandas scikit-learn

import pandas as pd
import numpy as np
import shutil
import tensorflow as tf
from transformers import AutoTokenizer, TFBertForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy
from google.colab import files

df = pd.read_csv("dataset_ic.csv")
df

model_name = "indobenchmark/indobert-base-p1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFBertForSequenceClassification.from_pretrained(model_name, num_labels=3)

sentences = df['topic'].tolist()
labels = df['intent'].tolist()

def encode_texts(texts, tokenizer, max_length=64):
  encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_length, return_tensors="tf")
  return encodings['input_ids'], encodings['attention_mask']

input_ids, attention_masks = encode_texts(sentences, tokenizer)

labels = tf.convert_to_tensor(labels)

input_ids_np = input_ids.numpy()
attention_masks_np = attention_masks.numpy()
labels_np = labels.numpy()

train_ids, val_ids, train_masks, val_masks, train_labels, val_labels = train_test_split(
    input_ids_np, attention_masks_np, labels_np, test_size=0.2, random_state=42
)

train_ids = tf.convert_to_tensor(train_ids)
val_ids = tf.convert_to_tensor(val_ids)
train_masks = tf.convert_to_tensor(train_masks)
val_masks = tf.convert_to_tensor(val_masks)
train_labels = tf.convert_to_tensor(train_labels)
val_labels = tf.convert_to_tensor(val_labels)

train_dataset = tf.data.Dataset.from_tensor_slices(({
    "input_ids":train_ids,
    "attention_mask": train_masks
  }, train_labels))

val_dataset = tf.data.Dataset.from_tensor_slices(({'input_ids': val_ids, 'attention_mask': val_masks}, val_labels))

batch_size=8
train_dataset = train_dataset.shuffle(100).batch(batch_size)
val_dataset = val_dataset.batch(batch_size)

optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5)
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

patience = 3
min_delta = 1e-4
best_val_loss = float('inf')
wait = 0

epochs = 10
for epoch in range(epochs):
    print(f"Epoch {epoch + 1}/{epochs}")

    train_loss_total = 0
    train_steps = 0

    for step, (x_batch_train, y_batch_train) in enumerate(train_dataset):
        with tf.GradientTape() as tape:
            logits = model(x_batch_train, training=True).logits
            loss_value = loss_fn(y_batch_train, logits)

        grads = tape.gradient(loss_value, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        train_loss_total += loss_value
        train_steps +=1

        if step % 50 == 0:
            print(f"Training loss at step {step}: {loss_value:.4f}")

    train_loss_avg = train_loss_total / train_steps


    val_loss_total = 0
    val_steps = 0
    for x_batch_val, y_batch_val in val_dataset:
        val_logits = model(x_batch_val, training=False).logits
        val_loss_total += loss_fn(y_batch_val, val_logits)
        val_steps += 1

    val_loss_avg = val_loss_total / len(val_dataset)

    print("====================================================")
    print(f"Training loss: {train_loss_avg: .4f}")
    print(f"Validaiton loss: {val_loss_avg: .4f}")
    print("====================================================")

    if val_loss_avg < best_val_loss - min_delta:
      best_val_loss = val_loss_avg
      wait = 0
      print("Validation loss improved")
    else:
      wait +=1
      print(f"No improvement in validation loss. Patience: {wait}/{patience}")

    if wait >= patience:
      print("Early stoping triggered, Stopping training...")
      break

preds = model.predict(val_dataset)
pred_labels = tf.argmax(preds.logits, axis=1).numpy()

true_labels = []
for _, label in val_dataset:
    true_labels.extend(label.numpy())
true_labels = np.array(true_labels)

target_names = ['Alergi', 'Obat', 'Menstruasi']
print(classification_report(true_labels, pred_labels, target_names=target_names))

test_text = "salep yang cocok untuk alergi "

test_encodings = tokenizer(test_text, truncation=True, padding=True, max_length=128, return_tensors="tf")

preds = model(test_encodings)
pred_label = tf.argmax(preds.logits, axis=1).numpy()[0]

label_mapping = {0: "alergi", 1: "obat", 2: "menstruasi"}
print(f"Predicted label: {label_mapping[pred_label]}")

model.save_pretrained('fine_tuned_indobert')
tokenizer.save_pretrained('fine_tuned_indobert')

shutil.make_archive('fine_tuned_indobert', 'zip', 'fine_tuned_indobert')
files.download('fine_tuned_indobert.zip')