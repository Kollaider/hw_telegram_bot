import re
import telebot
import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

bot = telebot.TeleBot(TOKEN)


def contains_url(message):
    url_regex = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    return re.search(url_regex, message.text) is not None


def handle_url_message(message):
    bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Ваша ссылка получена и отправлена на проверку.")


@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    if contains_url(message):
        handle_url_message(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте ваше домашнее задание в виде файла или ссылки на репозиторий.")


@bot.message_handler(content_types=['text'])
def handle_url_message(message):
    bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Ваша ссылка получена и отправлена на проверку.")



@bot.message_handler(content_types=['document'])
def handle_docs(message):
    # Check if user is admin
    if message.chat.id == ADMIN_CHAT_ID:
        bot.send_message(message.chat.id, "Вы администратор, ваш файл сохранён.")
    else:
        # Send file to admin
        bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Ваше домашнее задание получено и отправлено на проверку.")


if __name__ == '__main__':
    bot.polling(none_stop=True)
