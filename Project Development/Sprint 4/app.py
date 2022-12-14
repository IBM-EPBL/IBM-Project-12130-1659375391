from flask import Flask, render_template, request
import numpy as np
import pickle
import requests

API_KEY = "MiEIXgOPIbVeaUqt29RlxgPJZgi32ziBkiedChxOcyE7"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)

def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list)
    loaded_model = pickle.load(open("Car Resale Value Prediction.pkl", "rb"))
    result = loaded_model.predict([to_predict])
    return result[0]


@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/login', methods =['POST'])#binds to an url
def login():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
        
        payload_scoring = {"input_data": [{"fields": [['f0','f1','f2','f3','f4','f5', 'f6','f7','f8', 'f9']], "values": to_predict_list}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/af950cfc-9c0f-445b-9989-e7d91b3024f4/predictions?version=2022-11-07', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        
        return render_template("index.html",y = "The Value of the Car is :   " + str(result) )

@app.route('/admin')#binds to an url
def admin():
    return "Hey Admin How are you?"

if __name__ == '__main__' :
    app.run(debug= True)
    
    