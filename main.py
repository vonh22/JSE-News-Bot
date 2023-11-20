import telebot
import threading

from scrape import *
from users import *
from calculatetimeout import *

article_title = "<b>JAMAICA STOCK EXCHANGE </b>"

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)


def send_news_articles():
    while True:
        new_articles = get_jse_news_articles()
        users = getusers()
        if new_articles:
            for article in new_articles:
                for user in users:
                    bot.send_message(chat_id=user, text=F"{article_title} \n"
                                                        "\n"
                                                        F"{article}", parse_mode='HTML')
            maintenance()
        time.sleep(calculate_time_out())


news_thread = threading.Thread(target=send_news_articles)
news_thread.daemon = True  # This will allow the thread to exit when the main program exits
news_thread.start()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     F"Hello! I'm a bot that sends news articles from the Jamaica Stock Exchange to individuals who "
                     F"request them.\n"
                     "\n"
                     "<b>Here is a list of my commands: </b> \n"
                     "<b>/add</> - To have articles sent to you.\n"
                     "<b>/delete</> - To stop receiving articles. ", parse_mode='HTML')


@bot.message_handler(commands=['addUser'])
def start(message):
    if finduser(message.chat.id) == 1:
        adduser(message.chat.id)
        bot.send_message(message.chat.id, F"You have been successfully added.")
    else:
        bot.send_message(message.chat.id, F"You have already been added.")


@bot.message_handler(commands=['deleteUser'])
def delete(message):
    if finduser(message.chat.id) > 1:
        deleteuser(message.chat.id)
        bot.send_message(message.chat.id, 'Alright, you will no longer receive JSE news articles.')
        bot.send_message(message.chat.id, "Please note that if you would like to resume receiving articles, you can"
                                          " simply use the \n"
                                          "/addUser command.")

    else:
        bot.send_message(message.chat.id, "You are currently not registered as a user.")


bot.infinity_polling()

