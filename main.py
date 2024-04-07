import os
import telebot
import requests
import json
import math
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))
API = 'd1445c5cdcc719f8cda85ac8ed62bb9b'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.username}! Please write your city.')

@bot.message_handler(content_types=['text'])
def get_weather (message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']
        wind = data['wind']['speed']
        
        bot.reply_to(message, f'Weather now: {math.trunc(temp)}°C\nWind speed now: {math.trunc(wind)} m/s')
        
        if wind < 20 and data["weather"][0]['main'] == 'Clear':
            bot.send_message(message.chat.id, "The weather is perfect for a walk now!")
            bot.send_sticker(message.chat.id, open('./images/perfect_weather.png', 'rb'))
        elif data["weather"][0]['main'] == "Rain":
            bot.send_message(message.chat.id, "It's a rainy day! Dont't forget your umbrella!")
            bot.send_sticker(message.chat.id, open('./images/rainy_weather.png', 'rb'))     
        elif data["weather"][0]['main'] == "Snow":
            bot.send_message(message.chat.id, "It's a snowy day!")
            bot.send_sticker(message.chat.id, open('./images/snowy_weather.png', 'rb'))
    else: 
        bot.reply_to(message, 'Invalid city name! Try again!')

bot.polling(non_stop=True)