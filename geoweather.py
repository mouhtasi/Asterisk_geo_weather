import re
import sys
import pygeoip

def get_coordinates(ip):
    '''Get longitude and latitude from the ip address with GeoIP.'''
    gi = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)
    record = gi.record_by_addr(ip)
    lat, long = record['latitude'], record['longitude']
    return lat, long

if __name__ == '__main__':

    if len(sys.argv)> 1:
        ip = sys.argv[1]
        if not re.match(r'[0-9]+(?:\.[0-9]+){3}', ip):
            print 'Input is not a valid IP address!'
            exit(2)
    else:
        print 'Missing IP address input!'
        exit(2)

    lat, long = get_coordinates(ip)
