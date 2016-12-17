#!/usr/bin/env python
"""Scrape listings"""

import sys
import crawler

def main():
    """Entry point into scraping all listings on all pages"""
    url = sys.argv[1]
    listings_per_page = sys.argv[2]
    homes_list = []
    # First iteration to retrieve record/pagination info and scrape first page listings
    page_spider = get_page_spider(url, listings_per_page)
    collect_listing_objects(page_spider, homes_list)
    records = set_pagination_data(get_records_spider(page_spider))
    for num in xrange(records["total_pages"]): # Subsequent iterations with pagination urls
        paginated_page_spider = get_page_spider(url + '/page/' + str(num+1), listings_per_page)
        collect_listing_objects(paginated_page_spider, homes_list)

def collect_listing_objects(page_spider, homes_list):
    """Add listing derived from each page's listings' markup to total list"""
    listing_spiders = page_spider.find_all('div', class_="summary")
    for listing_spider in listing_spiders:
        homes_list.append(set_listing_obj(listing_spider))

def set_listing_obj(listing_spider):
    """Collect details to instantiate and set values for a listing object"""
    listing = Listing() # Create a new listing object
    general_class_spider = listing_spider.find(class_="left")
    info_class_spider = listing_spider.find(class_="right").find(class_="info")
    listing.listing_id = str(listing_spider['id'].split('_')[2])
    listing.name = str(general_class_spider.find(class_="title").h3.a.string)
    listing.categories = get_listing_categories(general_class_spider.find(class_="title").p)
    listing.description = str(general_class_spider.p.string)
    set_listing_address(listing, info_class_spider.address.find_all('span'))
    set_contact_info(listing, info_class_spider.find_all('p'))
    return listing

def set_contact_info(listing, contact_spiders):
    """Set phone, fax and website for a listing"""
    for contact_spider in contact_spiders:
        if contact_spider['class'] == 'claim': # Listings are unverified when they can be claimed
            listing.verified = False
        if "phone" in str(contact_spider.strong.string): # Set phone
            listing.phone = str(contact_spider.find(class_="hide").string)
        elif "fax" in str(contact_spider.strong.string): # Set fax
            listing.fax = str(contact_spider.find(class_="hide").string)
        elif "website" in str(contact_spider.strong.string): # Set website
            listing.website = str(contact_spider.a['title'])

def set_listing_address(listing, addr_spans_spider):
    """Set locality and address string for a listing"""
    span_count = len(addr_spans_spider)
    # Span count should be 2, can be 3 when address includes floor or suite
    listing.address = str(addr_spans_spider[0].string).strip()
    if span_count > 2:
        listing.address += " " + str(addr_spans_spider[1].string).strip()
        locality = str(addr_spans_spider[2].string).split(',')
    else:
        locality = str(addr_spans_spider[1].string).split(',')
    listing.city = locality[0].strip()
    listing.state = locality[1].strip()
    listing.zip = locality[2].strip()
    if listing.address and listing.city:
        geocode_address(listing)

def geocode_address(listing):
    """Geocode addresses to lat/lon"""
    pass

def get_listing_categories(category_spider):
    """Return array of categories which listing belongs to"""
    categories = []
    for category in category_spider.find_all('a'):
        if category['title']: # Avoid href with title, they represent non-category items
            continue
        categories.append(str(category.string))
    return categories

def get_records_spider(page_spider):
    """Retrieve spider regarding listings and pagination"""
    return page_spider.find(class_="filter").find(class_="right").find_all('strong')

def set_pagination_data(records_spider):
    """Set records and page data"""
    records = {}
    records["total_records"] = int(records_spider[0].string)
    records["current_page"] = int(records_spider[1].string)
    records["total_pages"] = int(records_spider[2].string)
    return records

def get_page_spider(url, listings_per_page):
    """Provide the spider derived from the webpage"""
    return crawler.parse_markup(url, listings_per_page)

class Listing(object):
    """Represents a home listing"""
    def __init__(self):
        self.listing_id = None
        self.name = None
        self.description = None
        self.categories = []
        self.address = None
        self.neighborhood = None
        self.county = None
        self.city = None
        self.state = None
        self.zip = None
        self.phone = None
        self.fax = None
        self.website = None
        self.lat = None
        self.lon = None
        self.verified = True
