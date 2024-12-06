# Bot Telegram

Este projeto é um bot para Telegram, desenvolvido em Python, que utiliza a biblioteca `python-telegram-bot` para gerenciar interações com a API do Telegram. Ele permite conversão de moedas, visualização de cotações e exibição de informações sobre moedas disponíveis.

## Requisitos

- Python 3.8 ou superior
- Conta no Telegram para criar um bot
- Token de API do Telegram Bot (obtido através do BotFather)
- Biblioteca `python-telegram-bot`
- Biblioteca `python-dotenv`
- Biblioteca `requests`

## Configuração do Ambiente

#1. **Clone este repositório:**
   ```bash

git clone https://github.com/NathanAzvdo/chatbot_py

``` 

#2. **Crie um ambiente virtual:**
   ```bash
python -m venv myenv
source myenv/bin/activate  # No Windows: myenv\Scripts\activate
```

#3. **Instale as dependências:**
   ```bash
pip install -r requirements.txt
```

#4. **Configure o arquivo `.env`:**
   Crie um arquivo `.env` na raiz do projeto e adicione o seguinte conteúdo:
   ```
   TELEGRAM_BOT_TOKEN=SEU_TOKEN_AQUI
   COINS_API=URL_DA_API_DE_COTACOES
   ```

## Estrutura do Projeto

- `main.py`: Ponto de entrada do bot. Carrega o token do Telegram do arquivo `.env` e inicia o bot.
- `bot/botTelegram.py`: Contém a classe `TelegramBot`, responsável por:
  - Gerenciar os comandos e mensagens recebidas.
  - Processar conversões de moeda.
  - Exibir cotações e moedas disponíveis.
  - Usar os utilitários de formatação e cálculo.
- `bot/coinAPI_factory.py`: Define a classe `CoinsAPIFactory`, que fornece uma instância da API de cotações configurada.
- `bot/coinAPI.py`: Contém a classe `CoinsAPI`, que lida com requisições para obter cotações de moedas.
- `bot/formatters/message_formatter.py`: Define as classes `MessageFormatter` (formata mensagens de resposta) e `ConversionCalculator` (realiza cálculos de conversão de moeda).
- `messages.json`: Contém mensagens predefinidas para respostas do bot.
- `moedas.json`: Lista de moedas suportadas com descrições.
- `.env`: Arquivo de configuração para variáveis sensíveis, como tokens e URLs de API.

## Execução do Bot

#1. Certifique-se de que todas as dependências estão instaladas e o arquivo `.env` está configurado.

#2. Execute o bot:
   ```bash
python main.py
```

Se o token estiver ausente ou incorreto, o programa lançará um erro:
```python
raise ValueError("Telegram bot token não encontrado no arquivo .env")
```

## Funcionalidades

- **/converter**: Converte valores entre duas moedas.
  - Exemplo: `/converter 100 USD-BRL` converte 100 dólares para reais.
- **/moedas**: Lista as moedas disponíveis para conversão.
- **/cotacao**: Exibe informações detalhadas de cotação entre duas moedas.
  - Exemplo: `/cotacao USD-BRL` mostra a taxa de câmbio atual de dólar para real.