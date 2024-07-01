import telebot
import json
from dotenv import load_dotenv
import os
import re
from .coinAPI import CoinsAPI

class TelegramBot:
    def __init__(self, bot_key):
        self.bot = telebot.TeleBot(bot_key)
        self.coins_info = CoinsAPI()

        with open("messages.json", "r", encoding="utf-8") as file1, open("moedas.json", "r", encoding="utf-8") as file2:
            self.bot_message = json.load(file1)
            self.moedas_disponiveis = json.load(file2)

        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=["converter"])
        def converter(mensagem):
            try:
                amount, base_currency, target_currency = self.parse_conversion_command(mensagem.text)
                buscaCotacao = self.coins_info.return_cotation(base_currency.upper(), target_currency.upper())
                valor = self.calcularConversao(buscaCotacao, int(amount))
                msg = self.formata_mensagem_conversao(json.loads(buscaCotacao), valor)
                if valor and msg:
                    self.bot.send_message(mensagem.chat.id, msg)
                else:
                    self.bot.send_message(mensagem.chat.id, self.bot_message["mensagem_erro"])
            except Exception as e: 
                print(e)
                self.bot.send_message(mensagem.chat.id, self.bot_message["mensagem_erro"])
        
        @self.bot.message_handler(commands=["moedas"])
        def moedas(mensagem):
            try:
                msg = self.moedas_disponiveis["mensagem"]
                moedas_lista = self.moedas_disponiveis["moedas"]
                texto_mensagem = f"{msg}\n\n"
                for chave, valor in moedas_lista.items():
                    texto_mensagem += f"{chave}: {valor}\n"
                self.bot.send_message(mensagem.chat.id, texto_mensagem)
            except Exception as e:
                self.bot.send_message(mensagem.chat.id, self.bot_message["mensagem_erro"])

        @self.bot.message_handler(commands=["cotacao"])
        def cotacao(mensagem):
            try:
                moeda = self.separar_moedas_msg(mensagem)
                if moeda:
                    moeda1, moeda2 = moeda
                    info = self.coins_info.return_cotation(moeda1.upper(), moeda2.upper())
                    msg = self.formata_mensagem_cotacao(json.loads(info))
                    self.bot.send_message(mensagem.chat.id, msg)
                else:
                    self.bot.send_message(mensagem.chat.id, self.bot_message["mensagem_erro"])
            except Exception as e:
                self.bot.send_message(mensagem.chat.id, self.bot_message["mensagem_erro"])

        @self.bot.message_handler(func=self.verificar)
        def responder_mensagem(mensagem):
            self.bot.reply_to(mensagem, self.bot_message["mensagem_receptiva"])

    def formata_mensagem_cotacao(self, informacoes):
        msg = self.bot_message["mensagem_cotacao"].format(
            nome=informacoes["nome"],
            bid=informacoes["bid"],
            ask=informacoes["ask"],
            alta=informacoes["alta"],
            baixa=informacoes["baixa"]
        )
        return msg

    def formata_mensagem_conversao(self, informacoes, valor):
        msg = self.bot_message["mensagem_conversao"].format(
            nome=informacoes["nome"],
            bid=informacoes["bid"],
            ask=informacoes["ask"],
            alta=informacoes["alta"],
            baixa=informacoes["baixa"],
            conv=valor
        )
        return msg

    def parse_conversion_command(self, command):
        pattern = r'/converter (\d+(?:\.\d+)?) (\w+)-(\w+)'
        match = re.match(pattern, command)
        
        if match:
            amount = float(match.group(1))
            base_currency = match.group(2)
            target_currency = match.group(3)
            return amount, base_currency, target_currency
        else:
            return None, None, None

    def calcularConversao(self, cotacao, valor):
        try:
            valorMoeda = json.loads(cotacao)
            venda = float(valorMoeda["ask"])
            valorFinal = float(valor) * venda
            return valorFinal
        except Exception as e:
            print(f"Erro ao calcular conversão: {e}")
            return None

    def separar_moedas_msg(self, msg):
        partes = msg.text.split()
        if len(partes) == 2 and '-' in partes[1]:
            moedaPrim = partes[1].split('-')[0]
            moedaSec = partes[1].split('-')[1]
            return moedaPrim, moedaSec
        else:
            return None

    def verificar(self, mensagem):
        return True

    def start(self):
        self.bot.polling()
