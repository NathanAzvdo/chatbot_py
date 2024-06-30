import telebot
import json
from dotenv import load_dotenv
import os
from coinAPI import CoinsAPI

coins_info = CoinsAPI()

with open("messages.json", "r", encoding="utf-8") as file1, open("moedas.json", "r", encoding="utf-8") as file2:
    bot_message = json.load(file1)
    moedas_disponiveis= json.load(file2)

load_dotenv()
    
    
bot_key = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(bot_key)

def verificar(mensagem):
    return True

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
        bot.send_message(mensagem.chat.id, f"Ocorreu um erro ao processar sua solicitação: {str(e)}")


@bot.message_handler(commands=["cotacao"])
def cotacao(mensagem):
        moeda = separar_moedas_msg(mensagem)
        if moeda:
            moeda1, moeda2 = moeda
            info = coins_info.return_cotation(moeda1, moeda2)
            msg = formata_mensagem_cotacao(json.loads(info))
            bot.send_message(mensagem.chat.id, msg)
        else:
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

