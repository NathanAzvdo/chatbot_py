import os
from dotenv import load_dotenv
import requests
from .coinAPI import CoinsAPI

class CoinsAPIFactory:
    def __init__(self):
        load_dotenv()

    def get_api(self):
        return CoinsAPI(os.getenv("COINS_API"))

