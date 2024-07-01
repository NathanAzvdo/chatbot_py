import unittest
from coinAPI import CoinsAPI
from unittest.mock import patch, MagicMock
import json

class CoinsAPI_Test(unittest.TestCase):
    
    coinAPI = CoinsAPI()

    @patch('requests.get')
    def test_return_cotation_success(self, mock_get):
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'USDBRL': {
                'name': 'Dollar/Real',
                'bid': '5.10',
                'ask': '5.15',
                'high': '5.20',
                'low': '5.00'
            }
        }
        mock_get.return_value = mock_response

        # Chama a função que você deseja testar
        result = CoinsAPI.return_cotation(None, 'USD', 'BRL')
        expected_result = json.dumps({
            'nome': 'Dollar/Real',
            'bid': '5.10',
            'ask': '5.15',
            'alta': '5.20',
            'baixa': '5.00'
        }, indent=4, ensure_ascii=False).encode('utf-8')

        
        self.assertEqual(result, expected_result)

    @patch('requests.get')
    def test_return_cotation_failure(self, mock_get):
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        
        result = CoinsAPI.return_cotation(None, 'USD', 'BRL')

        
        self.assertEqual(result, 'Erro ao acessar o URL: 404')

    @patch('requests.get')
    def test_return_cotation_exception(self, mock_get):
        
        mock_get.side_effect = Exception('Test Exception')

        result = CoinsAPI.return_cotation(None, 'USD', 'BRL')

        self.assertTrue(result.startswith('Erro:Test Exception'))

