#!/usr/bin/python
import re
import sys
import pygeoip
import requests

def get_coordinates(ip):
    '''Get longitude, latitude, city, and country from the ip address with
    GeoIP.'''
    gi = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)
    record = gi.record_by_addr(ip)
    lat, long, city = record['latitude'], record['longitude'], record['city']
    country = record['country_name']

    return lat, long, city, country

def get_weather_data(lat, long):
    '''Get the current JSON weather data from forecast.io with the personal API
        key.'''
    key = get_apikey()
    page = requests.get('https://api.forecast.io/forecast/' + key + '/'
                        + str(lat) + ',' + str(long)
                        +'?units=si&exclude=minutely,hourly,daily,alerts,flags')

    return page.json()['currently']

def get_apikey():
    '''Get the personal API key for forecast.io from file.'''
    try:
        f = open('api.keys')
    except:
        print 'Missing weather API key!'
    key = f.readline()
    f.close()
    return key

def parse_weather(data):
    '''Parse the JSON data and return the chosen weather data.'''
    temp = str(int(data['temperature']))
    humidity = str(int(data['humidity'] * 100))
    condition = str(data['summary'])
    wind = str(int(data['windSpeed'] * 3.6))                         # km/h
    bearing = str(data['windBearing'])
    pressure = str(round(data['pressure'] / 10, 2))                  # kPa

    return temp, humidity, condition, wind, bearing, pressure

if __name__ == '__main__':

    env = {}
    tests = 0;

    while 1:
        line = sys.stdin.readline().strip()
        if line == '':
            break

        ip = ''
        key, data = line.split(':')
        key = key.strip()
        data = data.strip()
        if key == 'agi_arg_1':
            ip = data

        if not ip:
            sys.stderr.write('No IP found.\n')
            sys.stderr.flush()
        else:
            lat, long, city, country = get_coordinates(ip)
            data = get_weather_data(lat, long)
            temp, humidity, condition, wind, bearing, pressure = parse_weather(data)

            sentence = ('Current weather in ' + city + ' ' + country + ' is '+ condition
                        + ', ' + temp + ' degrees Celcius with ' + humidity
                        + ' percent relative humidity. Wind speed is ' + wind
                        + ' kilometres per hour ' + 'bearing ' + bearing
                        + ' degrees with air pressure at ' + pressure + ' kilopascals.')

            sys.stdout.write('exec flite "' + sentence + '", any\n')
            sys.stdout.flush()
