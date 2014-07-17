import urllib
import csv
import logging

from grab.spider import Spider, Task

class YarSpider(Spider):
    initial_urls = ['http://realty.yandex.ru/search.xml?type=SELL&category=APARTMENT&roomsTotal=2&rgid=417899&metro=220']
    def prepare(self):
        self.result_file = csv.writer(open('result.txt', 'w')
    
    