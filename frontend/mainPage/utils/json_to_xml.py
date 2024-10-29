import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString


def json_to_xml(json_obj):
    """Convert JSON object to XML string."""
    elem = ET.Element("lista_respuestas")

    for item in json_obj:
        respuesta = ET.SubElement(elem, "respuesta")
        fecha = ET.SubElement(respuesta, "fecha")
        fecha.text = item["fecha"]

        mensajes = ET.SubElement(respuesta, "mensajes")
        for key, value in item["mensajes"].items():
            sub_elem = ET.SubElement(mensajes, key)
            sub_elem.text = str(value)

        analisis = ET.SubElement(respuesta, "analisis")
        for analisis_item in item["analisis"]:
            empresa = ET.SubElement(analisis, "empresa", nombre=analisis_item["nombre"])
            mensajes = ET.SubElement(empresa, "mensajes")
            for key, value in analisis_item["mensajes"].items():
                sub_elem = ET.SubElement(mensajes, key)
                sub_elem.text = str(value)

            servicios = ET.SubElement(empresa, "servicios")
            for servicio_item in analisis_item["servicios"]:
                servicio = ET.SubElement(
                    servicios, "servicio", nombre=servicio_item["nombre"]
                )
                mensajes = ET.SubElement(servicio, "mensajes")
                for key, value in servicio_item["mensajes"].items():
                    sub_elem = ET.SubElement(mensajes, key)
                    sub_elem.text = str(value)

    # Convertir el árbol XML a una cadena
    rough_string = ET.tostring(elem, encoding="unicode")
    # Formatear el XML
    reparsed = parseString(rough_string)

    return reparsed.toprettyxml(indent="  ")
