from datetime import date, datetime
import string
import json
import copy


class Service:
    def __init__(self, name, aliases):
        self.name = name
        self.aliases = aliases
        self.positive_messages = 0
        self.negative_messages = 0
        self.neutral_messages = 0
        self.total_messages = 0


class Company:
    def __init__(self, name, services):
        self.name = name
        self.services = services
        self.positive_messages = 0
        self.negative_messages = 0
        self.neutral_messages = 0
        self.total_messages = 0


class Dictionary:
    def __init__(self, possitive_sentiments, negative_sentiments, analize_companies):
        self.positive_sentiments = possitive_sentiments
        self.negative_sentiments = negative_sentiments
        self.analize_companies = analize_companies

    def copy(self):
        # Crear una nueva instancia de Dictionary con copias de los atributos
        return Dictionary(
            self.positive_sentiments.copy(),
            self.negative_sentiments.copy(),
            [
                Company(
                    company.name,
                    [
                        Service(service.name, service.aliases)
                        for service in company.services
                    ],
                )
                for company in self.analize_companies
            ],
        )


class Message:
    def __init__(self, message_data):
        self.date = None
        self.user = None
        self.social_network = None
        self.message = None
        self.positive_messages = 0
        self.negative_messages = 0
        self.neutral_messages = 0
        self.mentioned_companies = {}

        # Analizar el mensaje
        self.parse_message(message_data)

    def parse_message(self, message_data):
        # Extraer la fecha, usuario y red social del mensaje
        parts = message_data.split(" usuario: ")
        date_part = parts[0].split("lugar y fecha: ")[1].strip()
        user_part = parts[1].split(" red social: ")
        self.user = user_part[0].strip()
        social_network_part = user_part[1].split("\n")[0].strip()
        self.social_network = social_network_part
        self.message = user_part[1].split("\n", 1)[1].strip()

        # Convertir la fecha
        date_str = date_part.replace("guatemala, ", "").strip()
        self.date = datetime.strptime(date_str, "%d/%m/%Y %H:%M")

    def analyze_message(self, dictionary):
        translator = str.maketrans("", "", string.punctuation)
        normalized_message = self.message.translate(translator)
        words = normalized_message.split()

        positive_count = sum(
            1 for word in words if word in dictionary.positive_sentiments
        )
        negative_count = sum(
            1 for word in words if word in dictionary.negative_sentiments
        )

        if positive_count == negative_count:
            self.neutral_messages = 1
        elif positive_count > negative_count:
            self.positive_messages = 1
        else:
            self.negative_messages = 1

        # Analizar menciones de compañías
        for company in dictionary.analize_companies:
            company_mentions = sum(1 for word in words if word == company.name)
            if company_mentions > 0:
                if company.name not in self.mentioned_companies:
                    self.mentioned_companies[company.name] = 0
                self.mentioned_companies[company.name] += company_mentions

                company.total_messages += 1
                company.positive_messages += self.positive_messages
                company.negative_messages += self.negative_messages
                company.neutral_messages += self.neutral_messages


class DataAnalizeManager:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.data_analize_by_date = {}

    def add_message(self, message):
        newDictonary = self.dictionary.copy()
        message_date = message.date

        if message_date not in self.data_analize_by_date:
            self.data_analize_by_date[message_date] = DataAnalize(newDictonary, [])

        self.data_analize_by_date[message_date].lista_mensajes.append(message)

    def generate_json_response(self):
        response = []

        for date, data_analize in self.data_analize_by_date.items():
            date_response = {
                "fecha": date.strftime("%d/%m/%Y"),
                "mensajes": {
                    "total": data_analize.total_messages,
                    "positivos": data_analize.positive_messages,
                    "negativos": data_analize.negative_messages,
                    "neutros": data_analize.neutral_messages,
                },
                "analisis": [],
            }

            for company in data_analize.dictionary.analize_companies:
                company_data = {
                    "nombre": company.name,
                    "mensajes": {
                        "total": company.total_messages,
                        "positivos": company.positive_messages,
                        "negativos": company.negative_messages,
                        "neutros": company.neutral_messages,
                    },
                    "servicios": [],
                }

                for service in company.services:
                    service_data = {
                        "nombre": service.name,
                        "mensajes": {
                            "total": service.total_messages,
                            "positivos": service.positive_messages,
                            "negativos": service.negative_messages,
                            "neutros": service.neutral_messages,
                        },
                    }
                    company_data["servicios"].append(service_data)

                date_response["analisis"].append(company_data)

            response.append(date_response)

        return json.dumps(response, indent=4)


class DataAnalize:
    def __init__(self, dictionary, messages_list):
        self.dictionary = dictionary
        self.lista_mensajes = messages_list
        self.positive_messages = 0
        self.negative_messages = 0
        self.neutral_messages = 0
        self.total_messages = 0

    def analyze_messages(self):
        for message in self.lista_mensajes:
            self.total_messages += 1
            self.positive_messages += message.positive_messages
            self.negative_messages += message.negative_messages
            self.neutral_messages += message.neutral_messages

            for company in self.dictionary.analize_companies:
                if company.name in message.message:
                    for service in company.services:
                        for alias in service.aliases:
                            if alias in message.message:
                                service.total_messages += 1
                                service.positive_messages += message.positive_messages
                                service.negative_messages += message.negative_messages
                                service.neutral_messages += message.neutral_messages
                                break

    def generate_json_response(self):
        response = {
            "fecha": "01/04/2022",  # Puedes ajustar la fecha según sea necesario
            "mensajes": {
                "total": self.total_messages,
                "positivos": self.positive_messages,
                "negativos": self.negative_messages,
                "neutros": self.neutral_messages,
            },
            "analisis": [],
        }

        for company in self.dictionary.analize_companies:
            company_data = {
                "nombre": company.name,
                "mensajes": {
                    "total": company.total_messages,
                    "positivos": company.positive_messages,
                    "negativos": company.negative_messages,
                    "neutros": company.neutral_messages,
                },
                "servicios": [],
            }

            for service in company.services:
                service_data = {
                    "nombre": service.name,
                    "mensajes": {
                        "total": service.total_messages,
                        "positivos": service.positive_messages,
                        "negativos": service.negative_messages,
                        "neutros": service.neutral_messages,
                    },
                }
                company_data["servicios"].append(service_data)

            response["analisis"].append(company_data)

        return json.dumps(response, indent=4)
