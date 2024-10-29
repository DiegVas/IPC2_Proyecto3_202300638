from flask import Flask, request, jsonify
from utils.loadData import loadData

app = Flask(__name__)


app.secret_key = "mysecretkey"

# ! Global variables
AnalizeData = None

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/upload_xml', methods=['POST'])
def upload_xml():
    global AnalizeData
    print("upload_xml")
    request_data = request.get_json()
    AnalizeData = loadData(request_data)
    AnalizeData.analyze_messages()
    
    return jsonify({"message": "XML uploaded."})
    
    
if __name__ == '__main__':
    app.run(debug=True)