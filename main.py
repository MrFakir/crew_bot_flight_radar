import datetime
import traceback

from tele_bot import telegram_bot
from aircraft_park import park_aircraft
from threading import Thread


def main():
    try:
        # запуск потока на парсер парка
        t_one = Thread(target=park_aircraft)
        t_one.start()

        telegram_bot()
    except:
        with open('log_error_main.txt', 'a', encoding='utf-8') as file:
            file.write(str(datetime.datetime.now()) + ': ' + str(traceback.format_exc()) + '______\n')


if __name__ == '__main__':
    main()
