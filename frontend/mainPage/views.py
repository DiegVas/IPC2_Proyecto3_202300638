from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import xml.etree.ElementTree as ET
from mainPage.forms import XMLUploadForm
from pprint import pformat
from mainPage.utils.xml_Reader import xml_to_json
import requests

flaskAPI = "http://127.0.0.1:5000"


def home(request):
    return render(request, 'home.html')

def upload_xml(request):
    print ("upload_xml")
    if request.method == 'POST':
        form = XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                xml_file = request.FILES['xml_file']
                json_data = xml_to_json(xml_file)
                
                response = requests.post(flaskAPI + "/upload_xml", json=json_data)
                
                print (json_data)
                
                return render(request, 'home.html', {
                    'form': form,
                    'xml_result': pformat(json_data)
                })
                

                
            except Exception as e:
                messages.error(request, f'Error processing XML: {str(e)}')
        else:
            messages.error(request, 'Invalid form submission.')
    
    return redirect('home')

def query_data(request):
    if request.method == 'POST':
        # Aquí iría la lógica para consultar datos
        result = "Datos consultados..."
        return render(request, 'home.html', {
            'form': XMLUploadForm(),
            'query_result': result
        })
    return redirect('home')

def date_summary(request):
    if request.method == 'POST':
        # Aquí iría la lógica para el resumen por fecha
        result = "Resumen por fecha..."
        return render(request, 'home.html', {
            'form': XMLUploadForm(),
            'query_result': result
        })
    return redirect('home')

def range_summary(request):
    if request.method == 'POST':
        # Aquí iría la lógica para el resumen por rango
        result = "Resumen por rango..."
        return render(request, 'home.html', {
            'form': XMLUploadForm(),
            'query_result': result
        })
    return redirect('home')

def generate_pdf(request):
    if request.method == 'POST':
        # Aquí iría la lógica para generar PDF
        result = "Generando PDF..."
        return render(request, 'home.html', {
            'form': XMLUploadForm(),
            'query_result': result
        })
    return redirect('home')

def test_message(request):
    return render(request, 'home.html', {
        'form': XMLUploadForm(),
        'query_result': "Función de prueba de mensaje..."
    })
