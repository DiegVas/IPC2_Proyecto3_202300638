# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import xml.etree.ElementTree as ET
from pprint import pformat
from mainPage.utils.xml_Reader import xml_to_json
import requests
from mainPage.forms import AnalysisForm
from mainPage.utils.json_to_xml import json_to_xml
import json

flaskAPI = "http://127.0.0.1:5000"

xml_content = ""
xml_result = ""
companies = []
json_data = {}


def home(request):
    return render(request, "home.html")


def upload_xml(request):
    global xml_content, xml_result, companies, json_data
    first_text = ""
    if request.method == "POST":
        try:
            xml_file = request.FILES["xml_file"]
            json_data, xml_content = xml_to_json(xml_file)
            
            
            response = requests.post(flaskAPI + "/upload_xml", json=json_data)
            response_json = response.json()
            
            
            

            xml_result = ""
            companies = []

            if "data" in response_json:
                nested_json = json.loads(response_json["data"])
                companies = response_json["companies"]
                xml_result = json_to_xml(nested_json)
                print(companies)

            return render(
                request,
                "home.html",
                {
                    "first_text": xml_content,
                    "xml_result": pformat(json_data),
                    "second_text": xml_result,
                    "companies": companies,
                },
            )
        except Exception as e:
            messages.error(request, f"Error processing XML: {str(e)}")

    return redirect("home")


def query_data(request):
    if request.method == "POST":
        # Aquí iría la lógica para consultar datos
        result = "Datos consultados..."
        return render(request, "home.html", {"query_result": result})
    return redirect("home")


def date_summary(request):
    global xml_result
    if request.method == "POST":
        
        print(request.POST)
        fecha_seleccionada = request.POST.get('singleDate')
        companiesGet = request.POST.getlist('company')
        response = requests.post(flaskAPI + "/DateData", json={"date": fecha_seleccionada, "companies": companiesGet})
        response_json = response.json()
        
        if "data" in response_json:
            print(response_json)
            try:
                nested_json = json.loads(response_json["data"])
                xml_result = json_to_xml(nested_json)
            except Exception as e:
                xml_result = f"Error processing JSON: {str(e)}"
                    
        return render(
                request,
                "home.html",
                {
                    "first_text": xml_content,
                    "xml_result": pformat(json_data),
                    "second_text": xml_result,
                    "companies": companies,
                },
            )
    return redirect("home")


def range_summary(request):
    if request.method == "POST":
        print(request.POST)
        fecha_seleccionada = request.POST.get('dateRange')
        companiesGet = request.POST.getlist('company')
        fecha_seleccionada = fecha_seleccionada.split(" to ")
        response = requests.post(flaskAPI + "/RangeData", json={"date": fecha_seleccionada, "companies": companiesGet})
        response_json = response.json()
        
        if "data" in response_json:
            print(response_json)
            try:
                nested_json = json.loads(response_json["data"])
                xml_result = json_to_xml(nested_json)
            except Exception as e:
                xml_result = f"Error processing JSON: {str(e)}"
                    
        return render(
                request,
                "home.html",
                {
                    "first_text": xml_content,
                    "xml_result": pformat(json_data),
                    "second_text": xml_result,
                    "companies": companies,
                },
            )
    return redirect("home")


def generate_pdf(request):
    if request.method == "POST":
        # Aquí iría la lógica para generar PDF
        result = "Generando PDF..."
        return render(request, "home.html", {"query_result": result})
    return redirect("home")


def test_message(request):
    return render(
        request, "home.html", {"query_result": "Función de prueba de mensaje..."}
    )


def analysis_view(request):
    first_text = ""
    if request.method == "POST":
        if "xml_file" in request.FILES:
            xml_file = request.FILES["xml_file"]
            tree = ET.parse(xml_file)
            root = tree.getroot()
            # Extraer el contenido del archivo XML
            first_text = ET.tostring(root, encoding="unicode")

        form = AnalysisForm(request.POST)
        if form.is_valid():
            second_text = form.cleaned_data["second_text"]
            # Aquí puedes agregar la lógica para analizar los textos
    else:
        form = AnalysisForm()

    return render(request, "home.html", {"form": form, "first_text": first_text})
