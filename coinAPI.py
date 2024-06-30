import requests
import xml.etree.ElementTree as ET
import json
from dotenv import load_dotenv
import os

class CoinsAPI:


    load_dotenv()
    url_connect_api = os.getenv("COINS_API")

    def return_url_coins(moedaPrim, moedaSec):
        url = (f"https://economia.awesomeapi.com.br/json/last/{moedaPrim}-{moedaSec}")
        return url
    
    def return_cotation(*args, **kwargs):
        try:
            moedaPrim = args[1]
            moedaSec = args[2]
            url = CoinsAPI.return_url_coins(moedaPrim, moedaSec)
            response = requests.get(url)

            if response.status_code == 200:

                dados = response.json()
                moeda = {
                    'nome': dados[f'{moedaPrim}{moedaSec}']['name'],
                    'bid': dados[f'{moedaPrim}{moedaSec}']['bid'],
                    'ask': dados[f'{moedaPrim}{moedaSec}']['ask'],
                    'alta': dados[f'{moedaPrim}{moedaSec}']['high'],
                    'baixa': dados[f'{moedaPrim}{moedaSec}']['low']
                }
                json_moeda = json.dumps(moeda, indent=4, ensure_ascii=False)
                return json_moeda.encode('utf-8')

            else:
                return f"Erro ao acessar o URL: {response.status_code}"
        except Exception as e:
            return f'Erro:{e}'