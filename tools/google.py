from urllib2 import *
from urllib import urlencode
import json
from dateutil.parser import *


class Google:
    # method to do a get request
    @staticmethod
    def url_request(url, params):
        f = urlopen(url + "?" + urlencode(params))
        return f.read().decode('utf-8')

    @staticmethod
    def search_location(l):
        # get the data from google
        k = 'AIzaSyBPyJUxp1dec8i5yqiUD-JUjnufesYFsQc'
        params = dict(input=l, types='geocode', language='en', sensor='true', key=k)
        req = Google.url_request('https://maps.googleapis.com/maps/api/place/autocomplete/json', params)
        return json.loads(req)['predictions']

    @staticmethod
    def day_in_history(date):
        day = parse(date)
        req = Google.url_request('http://history.muffinlabs.com/date/' + day.day + '/' + day.month)
        return json.loads(req)