import where_is_aircraft
import telebot
from auth_data import token
import datetime
from send_email import send_email_log_error, send_email_log_message


def telegram_bot():
    bot = telebot.TeleBot(token)
    #bot.get_updates(allowed_updates=["channel_post"])

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет, Я CrewBot. '
                                          'Введи бортовой номер самолёта и узнаешь где он, пока это всё что я могу. '
                                          'Скоро будет больше бесполезных функций :)')

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        if message.text == 'log':
            bot.send_message(message.chat.id, send_email_log_message())
            bot.send_message(message.chat.id, send_email_log_error())
        else:
            # message_number_aircraft = where_is_aircraft.cool_aircraft_name(message.text)
            # bot.send_message(message.chat.id, where_is_aircraft.where_aircraft(message_number_aircraft),
            #                  parse_mode='HTML')
            bot.send_message(message.chat.id, where_is_aircraft.where_aircraft(message.text),
                             parse_mode='HTML')

            write_dump = str(datetime.datetime.fromtimestamp(message.date).strftime(
                "%d.%m.%Y %H:%M:%S")) + ': ' + str(message.from_user.id) + ' ' + message.text + '\n' + \
                         '_______________________________________' + '\n'
            try:
                with open('data/text_log.txt', 'a', encoding='utf-8') as file:
                    file.write(write_dump)
            except Exception as ex:
                print(ex)

    bot.polling()


def main():
    telegram_bot()


if __name__ == '__main__':
    main()
