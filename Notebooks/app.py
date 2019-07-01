
from flask import Flask, flash, jsonify, render_template, request
import webbrowser
from flask_cors import CORS, cross_origin
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
from keras.preprocessing.sequence import pad_sequences
from keras.backend import clear_session
from cypher import encode
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

app = Flask(__name__)
CORS(app)

# load the model, and pass in the custom metric function
with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
       model = load_model('third_model.h5')

model.summary()

global graph
graph = tf.get_default_graph()

@app.route('/')
def hello():
    # return "this webpage is working"
    return render_template('index.html')

@app.route('/handle_data', methods=['POST'])
def my_form_post():
    body = request.form['body']
    title= request.form['title']

    return f'Title:{title} and Body: {body}'

@app.route("/getvalue/<title>/<body>")
def data(title, body):
       body = body.replace("%20", " ")
       title = title.replace("%20", " ")
       tq = [{'Title':title,'Body':body}]
       df = pd.DataFrame(tq)

       df['indexed'] = df.apply(lambda x: encode(x['Title'], x['Body']), axis=1)
       final = pad_sequences(df['indexed'], value=0, padding='post', maxlen=50)
   
       global graph
       with graph.as_default():
              model._make_predict_function()
              f = model.predict_classes(final)

       prof = pd.read_csv("../Data/professionals_index_new.csv", header=None, names=["Profession", "Code"])
       data = prof.loc[prof["Code"] == f[0], "Profession"]
       
       try:
              return f'{data.values[0]}'
       except IndexError:
              return f'No professional match at this moment'
    
if __name__ == '__main__':
    app.run(debug=True)
