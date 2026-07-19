import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = "TOKEN"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для курса валют. Напиши /course")

@bot.message_handler(commands=['course'])
def course(message):
    try:
        url = "https://www.rbc.ru/quote/currency/?"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        usd_course = soup.find('span', class_='value')
        if usd_course:
            bot.send_message(message.chat.id, f"💵 Курс доллара: {usd_course.text.strip()} руб.")
        else:
            api_url = "https://api.exchangerate-api.com/v4/latest/USD"
            api_response = requests.get(api_url)
            data = api_response.json()
            rub_rate = data['rates']['RUB']
            bot.send_message(message.chat.id, f"💵 Курс доллара: {round(rub_rate, 2)} руб.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

bot.polling()
