from flask import Flask, request, jsonify
from utils.loadData import loadData
from utils.generateXML import generate_xml_response
from datetime import datetime
from classes.services import DataAnalizeManager, DataAnalize

app = Flask(__name__)


app.secret_key = "mysecretkey"

# ! Global variables
AnalizeData = None


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/upload_xml", methods=["POST"])
def upload_xml():
    global AnalizeData
    request_data = request.get_json()
    AnalizeData = loadData(request_data)
    json_response = AnalizeData.generate_json_response()

    # print(json_response)
    return jsonify({"data": json_response, "companies": [companies.name for companies in AnalizeData.dictionary.analize_companies]})

@app.route("/DateData", methods=["POST"])
def DateData():
    global AnalizeData
    selected_date = datetime.strptime(request.get_json()["date"], "%Y-%m-%d").date()
    selected_companies = request.get_json()["companies"]

    filterComanies = []
    filterAnalizeDataMana = DataAnalizeManager(AnalizeData.dictionary)
    filterAnalizeData = DataAnalize(AnalizeData.dictionary, [])
    for date_str, data_analize in AnalizeData.data_analize_by_date.items():
        if date_str == selected_date:
            for company in data_analize.dictionary.analize_companies:
                if company.name in selected_companies:
                    filterComanies.append(company)
            filterAnalizeData = data_analize
            filterAnalizeData.dictionary.analize_companies = filterComanies
            filterAnalizeDataMana.data_analize_by_date[date_str] = filterAnalizeData
    
    if not filterComanies:
        json_response = {"message": "No data available for the selected date."}
    else:
        json_response = filterAnalizeDataMana.generate_json_response()
        
    
    return jsonify({"data":json_response})


@app.route("/RangeData", methods=["POST"])
def RangeData():
    global AnalizeData
    selected_date = request.get_json()["date"]
    selected_companies = request.get_json()["companies"]
    start_date = datetime.strptime(selected_date[0], "%Y-%m-%d").date()
    end_date = datetime.strptime(selected_date[1], "%Y-%m-%d").date()

    filterComanies = []
    filterAnalizeDataMana = DataAnalizeManager(AnalizeData.dictionary)
    filterAnalizeData = DataAnalize(AnalizeData.dictionary, [])
    for date_str, data_analize in AnalizeData.data_analize_by_date.items():
        if date_str >= start_date and date_str <= end_date:
            for company in data_analize.dictionary.analize_companies:
                if company.name in selected_companies:
                    filterComanies.append(company)
            filterAnalizeData = data_analize
            filterAnalizeData.dictionary.analize_companies = filterComanies
            filterAnalizeDataMana.data_analize_by_date[date_str] = filterAnalizeData
    
    if not filterComanies:
        json_response = {"message": "No data available for the selected date range."}
    else:
        json_response = filterAnalizeDataMana.generate_json_response()
        
    
    return jsonify({"data":json_response})

if __name__ == "__main__":
    app.run(debug=True)
