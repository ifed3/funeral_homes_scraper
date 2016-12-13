#!/usr/bin/env python
"""Scrape listings"""

import sys
import crawler

def main():
    url = sys.argv[1]
    listings_per_page = sys.argv[2]
    page_spider = get_page_spider(url, listings_per_page)
    records_spider = get_records_spider(page_spider)
    records = set_pagination_data(records_spider)
    for num in xrange(records["total_pages"]):
        page_spider = get_page_spider(url + '/page/' + str(num), listings_per_page)

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
        self.address = None
        self.city = None
        self.state = None
        self.zip = None
        self.description = None
        self.phone = None
        self.fax = None
        self.website = None
        self.lat = None
        self.lon = None


