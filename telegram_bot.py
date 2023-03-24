import telebot
import json
import requests
import bs4
from datetime import timedelta, time
from telebot import types


bot = telebot.TeleBot('6201468316:AAFkeXdRarOJmy40l5Uu5drh-z14kF_6KQ8')


@bot.message_handler(commands=['tools'])
def tools(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    weather_forecast_button = types.KeyboardButton('Погода на сегодня')
    start_button = types.KeyboardButton('Старт')
    markup.add(weather_forecast_button, start_button)
    bot.send_message(message.chat.id, 'Выберите опцию', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Привет':
        bot.send_message(message.chat.id, "И вам того же", parse_mode='html')
    elif message.text == 'Фото':
        photo = open('cute_girl.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
    elif message.text == 'id':
        bot.send_message(message.chat.id, f"Твой ID: {message.from_user}", parse_mode='html')
    elif message.text == 'Старт':
        bot.send_message(message.chat.id, f"Здравствуйте, господин {message.from_user.first_name}", parse_mode = 'html')
    elif message.text == 'Погода на сегодня':
            def weather(url):
                req = requests.get(url)
                src = req.text
                # print(req)
                soup = bs4.BeautifulSoup(req.text, 'lxml')
                # print(soup)
                with open('weather.html', 'w') as file:
                    file.write(src)
                temperature = soup.find('div', class_="information__content__temperature").get_text(strip=True)
                print(temperature)
                other_data = soup.find('div',
                                       class_='information__content__additional information__content__additional_second'). \
                    find_all('div', class_='information__content__additional__item')
                # print(other_data)
                pressure = other_data[0].get_text(' ', strip=True)
                print(pressure)
                humidity = other_data[1].get_text(' ', strip=True)
                print(humidity)
                wind = other_data[2].get_text(' ', strip=True)
                print(wind)
                # ultraviolet_index = other_data[3].get_text(' ', strip=True)
                # print(ultraviolet_index)
                other_data_2 = soup.find_all('div', class_="information__content__additional__item__sun")
                # print(other_data_2)
                sunrise = other_data_2[0].get_text(' ', strip=True)
                sunset = other_data_2[1].get_text(' ', strip=True)
                print(sunset)
                print(sunrise)
                all_data = f"температура: {temperature} \nдавление : {pressure} \nвлажность: {humidity} \nветер : {wind} \nвосход: {sunrise} \nзакат: {sunset}"
                with open('weather/weather_datas.json', 'w', encoding='utf-8') as file:
                    json.dump(all_data, file, indent=4, ensure_ascii=False)

            weather('https://pogoda.mail.ru/prognoz/ufa/')

            weather_data = open('weather/weather_datas.json', 'rb')
            data = json.load(weather_data)
            # for key, value in data.items():
            bot.send_message(message.chat.id, data, parse_mode='html')
            # timer = datetime.datetime(2023, 3, 23, 16, 50, 0)
            # delta = timer - datetime.datetime.now()
            # time.sleep(delta.total_seconds())
            # print("Time expired!")
    else:
        bot.send_message(message.chat, "Я Вас не понимаю", parse_mode='html')
#       There's a bug in this code, but that's how it should be

# weather_forecast_time = time(5, 0, 0)

@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, "Классное фото")


bot.polling(none_stop=True)









# @bot.message_handler(commands=['website'])
# def website(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Посетить вебсайт", url='https://vk.com/overlod'))
#     bot.send_message(message.chat.id, "Перейти на вебсайт", reply_markup=markup)


# markup = types.InlineKeyboardMarkup()
#     weather_forecast_button = types.InlineKeyboardButton('weather_forecast_button',
#                                                          callback_data='weather_forecast_button')
#     markup.add(weather_forecast_button)


# @bot.callback_query_handler(func=lambda call: True)
# def handle_query(call):
#     if call.data == 'weather_forecast_button':
#         pass

# @bot.message_handler(commands=['tools'])
# def tools(message):
#     markup = types.InlineKeyboardMarkup()
#     weather_forecast_button = types.InlineKeyboardButton('Погода', callback_data="Вывести прогноз")
#     start_button = types.InlineKeyboardButton('Старт', callback_data='Поздороваться')
#     markup.row(weather_forecast_button, start_button)
#     bot.reply_to(message, 'Инструменты', reply_markup=markup)

