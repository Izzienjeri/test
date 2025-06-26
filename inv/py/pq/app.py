from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/data')
def get_data():
    data = {'name': 'John', 'age': 30}
    json_data = json.dumps(data)  # Convert to JSON string
    return jsonify(json_data=json_data)  # Wrap the JSON string in a Flask response object

if __name__ == '__main__':
    app.run()
