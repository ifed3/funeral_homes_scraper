"""Forward geocodes listings with addresses"""

import os
import time
import random
import geocoder
import listing_logger

OPENCAGE_API_KEY = os.environ['OPENCAGE_API_KEY']
BING_API_KEY = os.environ['BING_API_KEY']

class Geocoders(object):
    """List of geocoders to use and corresponding methods"""

    count_dict = {'total': 0, 'bing': 0, 'google': 0, 'opencage': 0}

    def __init__(self, address):
        self.address = address

    def geocode(self):
        """Return a geocoded object with location data"""
        rand_num = random.randint(0, 99)

        # Use bing 90% of time, google 7% and opencage 3% due to rate limiting factors
        if rand_num < 3: # Opencage
            return OpenCageGeocoder(self.address).geocode()
        elif rand_num < 10: # Google
            return GoogleGeocoder(self.address).geocode()
        else: # bing
            return BingGeocoder(self.address).geocode()

class GoogleGeocoder(Geocoders):
    """Google geocoder"""

    def __init__(self, address):
        return super(GoogleGeocoder, self).__init__(address)

    # Maximum of 2500 reqs per IP per day, 10 reqs/sec
    def geocode(self):
        time.sleep(0.25)
        Geocoders.count_dict['total'] += 1
        Geocoders.count_dict['google'] += 1
        return geocoder.google(self.address)

class BingGeocoder(Geocoders):
    """Bing geocoder"""

    def __init__(self, address):
        return super(BingGeocoder, self).__init__(address)

    # Official usage/limit policy both unclear and seemingly lax
    def geocode(self):
        Geocoders.count_dict['total'] += 1
        Geocoders.count_dict['bing'] += 1
        return geocoder.bing(self.address, key=BING_API_KEY)

class OpenCageGeocoder(Geocoders):
    """Opencage geocoder"""

    def __init__(self, address):
        return super(OpenCageGeocoder, self).__init__(address)

    #Maximum of 2500 reqs per api key per day, 1 req/sec
    def geocode(self):
        time.sleep(1)
        Geocoders.count_dict['total'] += 1
        Geocoders.count_dict['opencage'] += 1
        return geocoder.opencage(self.address, key=OPENCAGE_API_KEY)

logger = listing_logger.create_logger(__name__)        
