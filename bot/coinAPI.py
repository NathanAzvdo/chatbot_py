import requests


class CoinsAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def return_url_coins(self, moedaPrim, moedaSec):
        try:
            return f'{self.base_url}{moedaPrim}-{moedaSec}'
        except Exception as e:
            return f'Erro: {e}'
            
    def return_cotation(self, moedaPrim, moedaSec):
        try:
            url = self.return_url_coins(moedaPrim, moedaSec)
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
                return moeda
            else:
                return f"Erro ao acessar o URL: {response.status_code}"
        except Exception as e:
            return f'Erro:{e}'
