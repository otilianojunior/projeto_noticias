import json
import pymongo
import requests
from abc import ABC


class AbstractNoticias(ABC):

    def requisicao_site(url):
        try:
            data = {'url': url}
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            response = requests.post('http://0.0.0.0:8000/api_noticias/diarias', data=json.dumps(data), headers=headers)
            response_text = response.text
            return response_text
        except Exception:
            raise Exception


    def trasforma_dados(*args):
        try:
            dicionarios = []
            for response_text in args:
                dicionario = json.loads(response_text)
                dicionarios.append(dicionario)
            return dicionarios
        except Exception:
            raise Exception


    def salva_mongo(dicionarios):
        try:
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client['noticias-diarias-db']
            collection = db['noticias']
            result = collection.insert_many(dicionarios)
            print(f"Inserido no MongoDB: {result.inserted_ids}")
        except Exception:
            raise Exception
