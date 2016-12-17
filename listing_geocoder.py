"""Geocodes listings with addresses"""

import os
import time
from collections import namedtuple
import geocoder
import crawler

MAPZEN_API_KEY = os.environ['MAPZEN_API_KEY']
MAPBOX_TOKEN = os.environ['MAPBOX_TOKEN']
BING_API_KEY = os.environ['BING_API_KEY']

class Geocoders(object):
    """List of geocoders to use and corresponding methods"""

    count_dict = {'bing': 0, 'google': 0, 'opencage': 0}
    location = namedtuple("Location", "lat lon")

    def __init__(self, address):
        self.address = address

    def geocode(self):
        pass