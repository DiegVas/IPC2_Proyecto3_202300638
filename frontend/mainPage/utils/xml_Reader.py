# utils/xml_reader.py
import xml.etree.ElementTree as ET

def xml_to_json(xml_file):

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        data = {
            "diccionario": {
                "sentimientos_positivos": [],
                "sentimientos_negativos": [],
                "empresas_analizar": []
            },
            "lista_mensajes": []
        }
        
        diccionario = root.find('diccionario')
        if diccionario is not None:
            # ! Obtener sentimientos positivos
            sentimientos_pos = diccionario.find('sentimientos_positivos')
            if sentimientos_pos is not None:
                data["diccionario"]["sentimientos_positivos"] = [
                    palabra.text.strip() 
                    for palabra in sentimientos_pos.findall('palabra')
                    if palabra.text
                ]
            
            # ! Obtener sentimientos negativos
            sentimientos_neg = diccionario.find('sentimientos_negativos')
            if sentimientos_neg is not None:
                data["diccionario"]["sentimientos_negativos"] = [
                    palabra.text.strip() 
                    for palabra in sentimientos_neg.findall('palabra')
                    if palabra.text
                ]
            
            # ! Obtener empresas a analizar
            empresas = diccionario.find('empresas_analizar')
            if empresas is not None:
                for empresa in empresas.findall('empresa'):
                    emp_data = {
                        "nombre": empresa.find('nombre').text.strip() if empresa.find('nombre') is not None else "",
                        "servicios": []
                    }
                    
                    servicios = empresa.find('servicios')
                    if servicios is not None:
                        for servicio in servicios.findall('servicio'):
                            serv_data = {
                                "nombre": servicio.get('nombre', ''),
                                "alias": [
                                    alias.text.strip() 
                                    for alias in servicio.findall('alias')
                                    if alias.text
                                ]
                            }
                            emp_data["servicios"].append(serv_data)
                    
                    data["diccionario"]["empresas_analizar"].append(emp_data)
        
        # ! Obtener lista de mensajes
        lista_mensajes = root.find('lista_mensajes')
        if lista_mensajes is not None:
            data["lista_mensajes"] = [
                mensaje.text.strip() 
                for mensaje in lista_mensajes.findall('mensaje')
                if mensaje.text
            ]
        data = convert_to_lowercase(data)
        return data
    
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML format: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing XML: {str(e)}")
    
def convert_to_lowercase(data):
    if isinstance(data, dict):
        return {k: convert_to_lowercase(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_lowercase(item) for item in data]
    elif isinstance(data, str):
        return data.lower()
    else:
        return data

# Ejemplo de uso en el contexto del archivo xml_Reader.py
data = {
    "diccionario": {
        "sentimientos_positivos": [],
        "sentimientos_negativos": [],
        "empresas_analizar": []
    },
    "lista_mensajes": []
}
