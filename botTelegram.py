import telebot
import json
from dotenv import load_dotenv
import os
from coinAPI import CoinsAPI
import re

coins_info = CoinsAPI()

with open("messages.json", "r", encoding="utf-8") as file1, open("moedas.json", "r", encoding="utf-8") as file2:
    bot_message = json.load(file1)
    moedas_disponiveis= json.load(file2)

load_dotenv()
    
    
bot_key = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(bot_key)

def verificar(mensagem):
    return True

@bot.message_handler(commands=["converter"])
def converter(mensagem):
    try:
        amount, base_currency, target_currency = parse_conversion_command(mensagem.text)
        valor = calcularConversao(base_currency, target_currency, int(amount))
        if valor:
            bot.send_message(mensagem.chat.id, valor)
        else:
            bot.send_message(mensagem.chat.id, "lelelel")
    except Exception as e: 
        print(e)
        bot.send_message(mensagem.chat.id, "alalalla")
        
            
@bot.message_handler(commands=["moedas"])
def moedas(mensagem):
    try:
        msg = moedas_disponiveis["mensagem"]
        moedas_lista = moedas_disponiveis["moedas"]
        texto_mensagem = f"{msg}\n\n"
        for chave, valor in moedas_lista.items():
            texto_mensagem += f"{chave}: {valor}\n"
        bot.send_message(mensagem.chat.id, texto_mensagem)
    except Exception as e:
        bot.send_message(mensagem.chat.id, bot_message["mensagem_erro"])


@bot.message_handler(commands=["cotacao"])
def cotacao(mensagem):
        try:
            moeda = separar_moedas_msg(mensagem)
            if moeda:
                moeda1, moeda2 = moeda
                info = coins_info.return_cotation(moeda1.upper(), moeda2.upper())
                msg = formata_mensagem_cotacao(json.loads(info))
                bot.send_message(mensagem.chat.id, msg)
            else:
                bot.send_message(mensagem.chat.id, bot_message["mensagem_erro"])
        except Exception as e:
                bot.send_message(mensagem.chat.id, bot_message["mensagem_erro"])

def formata_mensagem_cotacao(informacoes):
    msg = bot_message["mensagem_cotacao"].format(
        nome= informacoes["nome"],
        bid= informacoes["bid"],
        ask= informacoes["ask"],
        alta= informacoes["alta"],
        baixa= informacoes["baixa"]
    )
    return msg

def parse_conversion_command(command):
    pattern = r'/converter (\d+(?:\.\d+)?) (\w+)-(\w+)'
    match = re.match(pattern, command)
    
    if match:
        amount = float(match.group(1))
        base_currency = match.group(2)
        target_currency = match.group(3)
        return amount, base_currency, target_currency
    else:
        return None, None, None

def calcularConversao(moedaB, moedaS, valor):
    try:
        buscaCotacao = coins_info.return_cotation(moedaB.upper(), moedaS.upper())
        valorMoeda = json.loads(buscaCotacao)  # Removido o .decode('utf-8'), pois loads já retorna um objeto Python
        venda = float(valorMoeda["ask"])
        valorFinal = float(valor)*venda
        return f"{valorFinal:.2f}"
    except Exception as e:
        print(f"Erro ao calcular conversão: {e}")
        return None


def separar_moedas_msg(msg):
    partes = msg.text.split()
    if len(partes) == 2 and '-' in partes[1]:
        moedaPrim = partes[1].split('-')[0]
        moedaSec = partes[1].split('-')[1]
        return moedaPrim, moedaSec
    else:
        return None


@bot.message_handler(func=verificar)
def responder_mensagem(mensagem):
    bot.reply_to(mensagem, bot_message["mensagem_receptiva"] )
    
    
bot.polling()

