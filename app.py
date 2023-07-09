from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(filename)
        # Process the CSV file
        with open(filename, 'r') as csv_file:
            csv_data = csv.reader(csv_file)
            for row in csv_data:
                # Process each row of the CSV file
                print(row)
        return 'CSV file uploaded and processed successfully.'
    else:
        return 'No file uploaded.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

