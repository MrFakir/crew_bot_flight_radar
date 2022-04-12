import datetime
from pyflightdata import FlightData
import json
import traceback
from send_email import send_email_log_error


def park_aircraft():  # сбор парка ак

    with open('data/temple_aircraft_park.json') as file:
        aircraft_list = json.load(file)
    return aircraft_list


def aircraft_data(number_aircraft):  # получение данных о самолете
    f = FlightData()
    fdata = f.get_history_by_tail_number(number_aircraft, limit=4)

    # with open('data/temple_aircraft_full_data.json', 'w') as file:
    #     json.dump(fdata, file, indent=4, ensure_ascii=False)
    #
    # with open('data/temple_aircraft_full_data.json', 'r') as file:
    #     fdata = json.load(file)

    return fdata


def where_aircraft(number_aircraft):  # получение данных, где самолёт из файла json
    try:
        if number_aircraft is not False:
            aircraft_data_local = aircraft_data(number_aircraft)
            index_number = 0
            while True:
                if aircraft_data_local[index_number]['airport']['destination'] == 'None' or \
                        (aircraft_data_local[index_number]['status']['text'].find('Estimated') == 0 and
                         aircraft_data_local[index_number]['status']['live'] == False):
                    index_number += 1
                    break
                else:
                    break
            status_aircraft = aircraft_data_local[index_number]['status']['live']
            last_destination = aircraft_data_local[index_number]['airport']['destination']['code']['iata']
            last_destination_name = aircraft_data_local[index_number]['airport']['destination']['name']
            last_from = aircraft_data_local[index_number]['airport']['origin']['code']['iata']
            last_from_name = aircraft_data_local[index_number]['airport']['origin']['name']
            flight_number = aircraft_data_local[index_number]['identification']['number']['default']
            destination_datetime_utc = aircraft_data_local[index_number]['status']['generic']['eventTime']['utc']
            destination_datetime_utc = datetime.datetime.fromtimestamp(destination_datetime_utc)
            time_now_utc = datetime.datetime.now()
            if status_aircraft is True:
                return (
                    f'Самолёт <b>{number_aircraft}</b> ещё летит рейсом <b>{flight_number}</b>\n'
                    '_____________\n'
                    f'из <b>{last_from}</b> - {last_from_name}\n'
                    f'в <b>{last_destination}</b> - {last_destination_name}.\n'
                    '_____________\n'
                    f'Прилетит в {destination_datetime_utc.strftime("<b>%H:%M:%S</b> %d.%m.%Y")} по UTC,\n'
                    f' через <b>{"Вот-вот прилетит, +- минутка (или уже рулит)" if str(destination_datetime_utc - time_now_utc)[0] == "-" else str(destination_datetime_utc - time_now_utc).split(".")[0]}</b>. '
                )
            else:
                return (
                    f'Самолет <b>{number_aircraft}</b> уже прилетел рейсом <b>{flight_number}</b>\n'
                    '______________\n'
                    f'из <b>{last_from}</b> - {last_from_name}\n'
                    f'в <b>{last_destination}</b> - {last_destination_name}'
                )
        else:
            return ('Кажется, вы не правильно ввели номер самолета. \n'
                    'Нужно ввести полное имя или такого самолёта нет :)')
    except:
        with open('logs/log_error.txt', 'a', encoding='utf-8') as file:
            file.write(str(datetime.datetime.now()) + ': ' + str(traceback.format_exc()) + '______\n')
        send_email_log_error()

        return 'Прости Бро, на сервере какая-то ошибка.' \
               'Мой папка обязательно с этим разберётся, очень скоро :)'


def cool_aircraft_name(aircraft_name):  # приводим в порядок имя
    aircraft_name = str(aircraft_name)
    if aircraft_name.replace('-', '').isalpha():
        aircraft_name = aircraft_name.upper()  # имя в верхний регистр
    else:
        return False

    if len(aircraft_name) == 5:
        aircraft_name = aircraft_name[:2] + '-' + aircraft_name[2:]
    if len(aircraft_name) == 6:
        aircraft_list = park_aircraft()
        if aircraft_name in aircraft_list:
            return aircraft_name
        else:
            return False
    else:
        return False


def main():
    input_aircraft_name = 'vpbmw'
    # aircraft_name = cool_aircraft_name(input_aircraft_name)
    print(where_aircraft(input_aircraft_name))


if __name__ == '__main__':
    main()
