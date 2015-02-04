#!/bin/python
import urllib
import csv
import logging
from grab.spider import Spider, Task
from grab.tools.logs import default_logging

class YarSpider(Spider):
	initial_urls = ['https://realty.yandex.ru/search?type=SELL&category=ROOMS&priceMax=1800000&currency=RUR&roomsTotal=2&roomsTotal=3&rgid=417899&metro=200&metro=216&metro=220&metro=235&metro=241&metro=245&metro=250']
	base_url = 'https://realty.yandex.ru'

	def prepare(self):
		self.result_file = csv.writer(open('result.txt', 'w'))

	def task_initial(self, grab, task):
		css_path = "a.b-pager__page"
		for elem in grab.css_list(css_path):
			yield Task('yarpage', url=elem.get('href'))

	def task_yarpage(self, grab, task):
		css_path = "div.b-serp-item__header a.b-link_redir_yes.stat.i-bem"

		print "Page body start"
		print grab.response.body
		print "Page body end"

		for elem in grab.css_list(css_path):
			print "Yar items from yarpage = "+elem.get('href')
			yield Task('yaritem', url=elem.get('href'))

	def task_yaritem(self, grab, task):
		print grab.response.url
		print grab.css_text(".offer-data__descr-item", default="No desc", smart=True, normalize_space=True)
		print grab.css_text(".seller__price", default="No price", smart=True, normalize_space=True)
		print grab.css_text(".offer-map__street", default="No street", smart=True, normalize_space=True)
		print grab.css_text(".offer-map__metro", default="No subway", smart=True, normalize_space=True)

if __name__ == '__main__':
	default_logging(grab_log='/tmp/grab.log', level=logging.DEBUG, mode='a',propagate_network_logger=False,network_log='/tmp/grab.network.log')
	bot = YarSpider()
	bot.run()
