from flask import Flask, render_template, request, jsonify
# import pickle
import joblib
import pandas as pd
import psycopg2
import os

app = Flask(__name__)


@app.route('/')
def home():
    '''
    # Using APScheduler
    url = "https://api.apilayer.com/currency_data/live"

    payload = {}
    headers= {
    "apikey": "mXqW3OZ5BMUuRd656pfVo7TZz8Rk1piF"
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    result = response.text
    res = json.loads(result)
    exchange_rate = res["quotes"]["USDCAD"]
    '''
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def web_post():
    if request.method =='POST':
        predict = None
        n1 = request.form['number1']
        n2 = request.form['number2']
        n3 = request.form['number3']
        n4 = request.form['number4']


        data = {'bathroomtotal': [n1],'parkingspacetotal': [n2],'longitude': [n3], 'latitude': [n4]}
        df = pd.DataFrame(data)

        predict = model.predict(df)
        return render_template('index.html', predict=predict)

@app.route("/database", methods=["GET"])
def web_mars_get():
    conn = psycopg2.connect("host=localhost dbname=project user=postgres password=5846 port=5432")
    cur = conn.cursor()
    cur.execute("""SELECT * FROM building b 
    LEFT JOIN property p USING (id)""")
    data_building = cur.fetchall()
    return jsonify({'msg': data_building})



if __name__ == '__main__':
    model = joblib.load(os.getcwd() + './model.pkl')
    # app.run('0.0.0.0', port=5000, debug=True)


