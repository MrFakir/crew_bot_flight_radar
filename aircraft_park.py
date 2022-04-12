from pyflightdata import FlightData
import json
import time


def park_aircraft():  # сбор парка ак
    while True:
        fdata = FlightData()
        fdata = fdata.get_fleet('u6-svr')
        aircraft_list = []
        for i in fdata:
            aircraft_list.append(i['reg'])
        with open('data/temple_aircraft_park.json', 'w') as file:
            json.dump(aircraft_list, file, indent=4, ensure_ascii=False)
        print('File of aircraft_park complete')
        time.sleep(43200)

def main():
    park_aircraft()


if __name__ == '__main__':
    main()