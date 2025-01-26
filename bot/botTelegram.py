import telebot
import json
from dotenv import load_dotenv
import os
import re
from .coinAPI_factory import CoinsAPIFactory
from .formatters.message_formatter import MessageFormatter, ConversionCalculator

class TelegramBot:
    def __init__(self, bot_key):
        self.bot = telebot.TeleBot(bot_key)
        self.api_factory = CoinsAPIFactory()
        self.coins_info = self.api_factory.get_api()
        self.formatter = MessageFormatter()
        self.calculator = ConversionCalculator()

        with open("messages.json", "r", encoding="utf-8") as file1, open("moedas.json", "r", encoding="utf-8") as file2:
            self.bot_message = json.load(file1)
            self.moedas_disponiveis = json.load(file2)

        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=["converter"])
        def converter(mensagem):
            try:
                amount, base_currency, target_currency = self.parse_conversion_command(mensagem.text)
                cotacao = self.coins_info.return_cotation(base_currency.upper(), target_currency.upper())
                valor = self.calculator.calcular(cotacao, int(amount))
                msg = self.formatter.format_conversion(cotacao, valor, self.bot_message["mensagens_info"])
                if valor and msg:
                    self.bot.send_message(mensagem.chat.id, msg)
                else:
                    self.bot.send_message(mensagem.chat.id, self.bot_message["mensagem_erro"])
            except Exception as e:
                print(e)
                self.bot.send_message(mensagem.chat.id, self.bot_message["mensagem_erro"])

        
        @self.bot.message_handler(commands=["get_chat_id"])
        def send_chat_id(message):
            chat_id = message.chat.id
            self.bot.reply_to(message, f"Seu chat ID é: {chat_id}")


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
                    msg = self.formatter.format_cotation(info, self.bot_message["mensagens_info"])
                    self.bot.send_message(mensagem.chat.id, msg)
                else:
                    self.bot.send_message(mensagem.chat.id, self.bot_message["mensagem_erro"])
            except Exception as e:
                self.bot.send_message(mensagem.chat.id, self.bot_message["mensagem_erro"])

        @self.bot.message_handler(func=self.verificar)
        def responder_mensagem(mensagem):
            self.bot.reply_to(mensagem, self.bot_message["mensagem_receptiva"])

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

    def start_keep_alive(self):
        def keep_alive():
            while True:
                try:
                    self.bot.send_chat_action(chat_id=os.getenv("CHAT_ID"), action="typing")
                    time.sleep(600)  # Mantém ativo a cada 10 minutos
                except Exception as e:
                    print(f"Erro no Keep-Alive: {e}")
                    time.sleep(60)  # Tenta novamente após 1 minuto

        threading.Thread(target=keep_alive, daemon=True).start()

    def start(self):
        self.start_keep_alive()
        self.bot.polling()