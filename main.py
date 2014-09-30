import urllib
import csv
import logging

from grab.spider import Spider, Task

class YarSpider(Spider):
    initial_urls = ['http://realty.yandex.ru/search.xml?type=SELL&category=APARTMENT&roomsTotal=2&rgid=417899&metro=220']
    def prepare(self):
        self.result_file = csv.writer(open('result.txt', 'w')
    
    def task_initial(self, grab, task):
	css_path = "html.i-ua_js_yes body.b-pagea div.b-wrapper div.b-layout div.b-serp-wrapper table.b-layout__table tbody tr td.b-layout__table-left div.b-pager div.b-pager__pages a.b-pager__page[href]"
	for elem in grab.css_list(css_path):
	    yield Task('yarpage', url=elem.get('href'))

    def task_yarpage(self,grab,task):
	css_path = "html.i-ua_js_yes body.b-pagea div.b-wrapper div.b-layout div.b-serp-wrapper table.b-layout__table tbody tr td.b-layout__table-left div.b-serp-list div.b-serp-item"
	for elem in grab.css_list(css_list):
	    
	

    
    