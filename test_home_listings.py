#!/usr/bin/env python

import unittest
from unittest import TestCase
import bs4
from home_listings import get_page_spider, get_records_spider

class TestPageContent(TestCase):
    def setUp(self):
        self.url = "http://funeralhomeresource.com/listing/guide/funeral-home"
        self.expected_listings = 10
        self.page_spider = get_page_spider(self.url, self.expected_listings)
        self.records_spider = get_records_spider(self.page_spider)

    def test_listings_count(self):
        self.assertEqual(len(self.page_spider.find_all(class_="summary")), self.expected_listings)

    def test_records_set_count(self):
        self.assertIsInstance(self.records_spider, bs4.element.ResultSet)
        self.assertEqual(len(self.records_spider), 3)

if __name__ == '__main__':
    unittest.main()