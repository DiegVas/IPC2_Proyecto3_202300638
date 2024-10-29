
from datetime import date, datetime
import string

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

class Message:
    def __init__(self, message_data, dictionary):
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
        self.analyze_message(dictionary)

    def parse_message(self, message_data):
        # Extraer la fecha, usuario y red social del mensaje
        parts = message_data.split(' usuario: ')
        date_part = parts[0].split('lugar y fecha: ')[1].strip()
        user_part = parts[1].split(' red social: ')
        self.user = user_part[0].strip()
        social_network_part = user_part[1].split('\n')[0].strip()
        self.social_network = social_network_part
        self.message = user_part[1].split('\n', 1)[1].strip()

        # Convertir la fecha
        date_str = date_part.replace("guatemala, ", "").strip()
        self.date = datetime.strptime(date_str, "%d/%m/%Y %H:%M")

    def analyze_message(self, dictionary):
        translator = str.maketrans('', '', string.punctuation)
        normalized_message = self.message.translate(translator)
        words = normalized_message.split()

        positive_count = sum(1 for word in words if word in dictionary.positive_sentiments)
        negative_count = sum(1 for word in words if word in dictionary.negative_sentiments)

        if positive_count == negative_count:
            self.neutral_messages = 1
        elif positive_count > negative_count:
            self.positive_messages = positive_count
        else:
            self.negative_messages = negative_count

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
            print(message.message)
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
