from flask import Flask, jsonify, request, render_template
import sqlite3
import jinja2
import pandas as pd
import os
import datetime
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

os.chdir(os.path.dirname(__file__))

app = Flask(__name__,template_folder='templates')
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>API TWITTER</h1><p>This site is a prototype API for sentimental prediction of tweets.</p>"

@app.route('/api/v1/create_db', methods=['GET'])
def createdb():
    con = sqlite3.connect('tweets_ver.db')
    cursor = con.cursor()
    cursor.execute("DROP TABLE IF EXISTS t;")
    cursor.execute("CREATE TABLE t (text, created_at, retweet_count, username, followers_count, verified);")
    df = pd.read_csv('tweets_ver.csv')
    for row in df.itertuples():
        cursor.execute('''
                    INSERT INTO t (text, created_at, retweet_count, username, followers_count, verified)
                    VALUES ('%s','%s','%s','%s','%s','%s')
                    ''' % (row.text, row.created_at, row.retweet_count, row.username, row.followers_count, row.verified)
                     )

    con.commit()
    results = cursor.execute("SELECT * FROM t;").fetchall()
    con.close()
    return jsonify(results)

# @app.route('/api/v1/new_register', methods=['POST'])
# def new_register():
#     con = sqlite3.connect('tweets.db')
#     cursor = con.cursor()

#     text = request.args.get('text', None)
#     created_at = request.args.get('created_at', None)
#     retweet_count = request.args.get('retweet_count', None)
#     username = request.args.get('username', None)
#     followers_count = request.args.get('followers_count', None)
#     verified = request.args.get('verified', None)
#     list_values = [text, created_at, retweet_count, username, followers_count, verified]

#     if text is None or created_at is None or retweet_count is None or username is None or followers_count is None or verified is None:
#         return "Args empty, the data were not stored"
#     else:
#         cursor.execute('INSERT INTO t (text, created_at, retweet_count, username, followers_count, verified) VALUES (?, ?, ? , ?, ?, ?);',list_values)
    
#     con.commit()
#     results = cursor.execute("SELECT * FROM t ORDER BY 1 ASC LIMIT 10;").fetchall()
#     con.close()
    
#     return jsonify(results)


@app.route('/api/v1/predict', methods=['GET'])
def predict():
    
    text = request.args.get('text', None)

    if text is None:
        return "Args empty, the data are not enough to predict"
    else:
        with open('finished.model', 'rb') as archivo_entrada:
            model = pickle.load(archivo_entrada)
        prediction = model.predict([text])
    
    return jsonify({'predictions': prediction[0]})




@app.route('/api/v1/predict_all', methods=['GET'])
def predict_all():
    
    data = pd.read_csv('tweets_ver.csv')
    data = data['text']

    if data is None:
        return "Args empty, the data are not enough to predict"
    else:
        with open('finished.model', 'rb') as archivo_entrada:
            model = pickle.load(archivo_entrada)
        data.to_json("test.json", orient = "records")
        with open('test.json', 'rb') as archivo:
            test = json.load(archivo)
            lst1 = []
            lst = []
            for x in test:
                r = model.predict([x])
                lst1.append(r[0])

    data = pd.DataFrame(data)
    data['polarity'] = lst1
    data['polarity'] = data['polarity'].map({'0':'Neg',
                             '1':'Pos',
                             np.nan:'--'},
                             na_action=None)


    return render_template('predict_all.html', tables=[data.to_html()], titles=[''])






@app.route('/api/v1/retrain', methods=['PUT'])
def retrain():
    con = sqlite3.connect('tweets_ver.db')
    cursor = con.cursor()
    data = cursor.execute('SELECT * FROM t').fetchall()
    con.close()

    data = pd.DataFqrame(data, columns= ['text'])

    X_train, X_test, y_train, y_test = train_test_split(data.drop(columns=['text']),
                                                        data['text'],
                                                        test_size = 0.20,
                                                        random_state=42)

    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)

    pickle.dump(lin_reg, open('tweets_ver.model', 'wb'))

    return "Finished train succesfully"

app.run()





