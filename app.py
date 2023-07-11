import pandas as pd
import json
import os
from flask import Flask, render_template, request
import csv

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024  # Limit file upload size to 1GB

def transform_dataframe_to_json(dataframe):
    data = []
    for _, row in dataframe.iterrows():
        prompt = row['prompt text']
        completion = row['ideal generated text']
        entry = {"prompt": prompt, "completion": completion}
        data.append(entry)
    return data

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded.'

    file = request.files['file']
    if file.filename == '':
        return 'No file selected.'

    # Check file size
    file_size = os.stat(file.filename).st_size
    if file_size > app.config['MAX_CONTENT_LENGTH']:
        return 'File size exceeds the limit of 1GB.'

    filename = file.filename
    file.save(filename)
    
    # Process the CSV file
    df = pd.read_csv(filename)
    trainingset = transform_dataframe_to_json(df)
    
    # Save JSON as 'trainingset' object
    app.trainingset = trainingset
    
    return 'CSV file uploaded and processed successfully.'

@app.route('/save_apikey', methods=['POST'])
def save_apikey():
    apikey = request.json.get('apikey')
    return '204'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


