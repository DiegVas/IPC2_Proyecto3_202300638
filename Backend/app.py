from flask import Flask, request, jsonify
from utils.loadData import loadData
from utils.generateXML import generate_xml_response

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
    request_data = request.get_json()
    AnalizeData = loadData(request_data)
    json_response = AnalizeData.generate_json_response()
    print(json_response)
   
    #print(json_response)
    return jsonify({"data":json_response})
    
    
if __name__ == '__main__':
    app.run(debug=True)