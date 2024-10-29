import xml.etree.ElementTree as ET

def generate_xml_response(data):
    root = ET.Element("lista_respuestas")

    respuesta = ET.SubElement(root, "respuesta")

    fecha = ET.SubElement(respuesta, "fecha")
    fecha.text = data["fecha"]

    mensajes = ET.SubElement(respuesta, "mensajes")
    total = ET.SubElement(mensajes, "total")
    total.text = str(data["mensajes"]["total"])
    positivos = ET.SubElement(mensajes, "positivos")
    positivos.text = str(data["mensajes"]["positivos"])
    negativos = ET.SubElement(mensajes, "negativos")
    negativos.text = str(data["mensajes"]["negativos"])
    neutros = ET.SubElement(mensajes, "neutros")
    neutros.text = str(data["mensajes"]["neutros"])

    analisis = ET.SubElement(respuesta, "analisis")
    for empresa in data["analisis"]:
        empresa_elem = ET.SubElement(analisis, "empresa", nombre=empresa["nombre"])

        mensajes_empresa = ET.SubElement(empresa_elem, "mensajes")
        total_empresa = ET.SubElement(mensajes_empresa, "total")
        total_empresa.text = str(empresa["mensajes"]["total"])
        positivos_empresa = ET.SubElement(mensajes_empresa, "positivos")
        positivos_empresa.text = str(empresa["mensajes"]["positivos"])
        negativos_empresa = ET.SubElement(mensajes_empresa, "negativos")
        negativos_empresa.text = str(empresa["mensajes"]["negativos"])
        neutros_empresa = ET.SubElement(mensajes_empresa, "neutros")
        neutros_empresa.text = str(empresa["mensajes"]["neutros"])

        servicios = ET.SubElement(empresa_elem, "servicios")
        for servicio in empresa["servicios"]:
            servicio_elem = ET.SubElement(servicios, "servicio", nombre=servicio["nombre"])

            mensajes_servicio = ET.SubElement(servicio_elem, "mensajes")
            total_servicio = ET.SubElement(mensajes_servicio, "total")
            total_servicio.text = str(servicio["mensajes"]["total"])
            positivos_servicio = ET.SubElement(mensajes_servicio, "positivos")
            positivos_servicio.text = str(servicio["mensajes"]["positivos"])
            negativos_servicio = ET.SubElement(mensajes_servicio, "negativos")
            negativos_servicio.text = str(servicio["mensajes"]["negativos"])
            neutros_servicio = ET.SubElement(mensajes_servicio, "neutros")
            neutros_servicio.text = str(servicio["mensajes"]["neutros"])

    return ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')