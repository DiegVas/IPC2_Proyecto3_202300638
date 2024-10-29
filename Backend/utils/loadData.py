from classes.services import Service, Company, Dictionary, Message, DataAnalize, DataAnalizeManager
from datetime import datetime


def loadData(json_data):
    # Crear objetos de Servicio a partir del JSON
    companies = []
    for company_data in json_data["diccionario"]["empresas_analizar"]:
        services = [Service(service["nombre"], service["alias"]) for service in company_data["servicios"]]
        company = Company(company_data["nombre"], services)
        companies.append(company)
    
    # Crear el objeto Diccionario
    dictionary = Dictionary(
        possitive_sentiments=json_data["diccionario"]["sentimientos_positivos"],
        negative_sentiments=json_data["diccionario"]["sentimientos_negativos"],
        analize_companies=companies
    )
    
    # Crear los objetos Mensaje a partir del JSON
    messages_list = []
    for message_data in json_data["lista_mensajes"]:
        message = Message(message_data)
        messages_list.append(message)
        
    manager = DataAnalizeManager(dictionary)
    
    for message in messages_list:
        manager.add_message(message)
    
    for date in manager.data_analize_by_date:
        
        for message in manager.data_analize_by_date[date].lista_mensajes:
            message.analyze_message(manager.data_analize_by_date[date].dictionary)
        
        manager.data_analize_by_date[date].analyze_messages()

    
    # Crear y devolver el objeto DataAnalyze
    return manager