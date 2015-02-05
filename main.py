#!/bin/python
import urllib

import time

import logging

from grab.spider import Spider, Task
from grab.tools.logs import default_logging
from grab.tools.lxml_tools import get_node_text
from grab.tools.lxml_tools import find_node_number

import saver
from saver import csvrowsaver
import csv
from csv import excel
from csv import register_dialect

class YarDic(excel):
	delimiter = '\t'

register_dialect("YarDic", YarDic)

class YarSpider(Spider):
	initial_urls = ['https://realty.yandex.ru/search?type=SELL&category=ROOMS&priceMax=1800000&currency=RUR&roomsTotal=2&roomsTotal=3&rgid=417899&metro=200&metro=216&metro=220&metro=235&metro=241&metro=245&metro=250']
	base_url = 'https://realty.yandex.ru'

	def prepare(self):
		self.csvfilesaver = csvrowsave.r('yar.json', ['price','header', 'link', 'adress', 'subway'], 'YarDic')

	def task_initial(self, grab, task):
		css_path = "a.b-pager__page"
		for elem in grab.css_list(css_path):
			yield Task('yarpage', url=elem.get('href'))

	def task_yarpage(self, grab, task):
		css_path = "div.b-serp-item__inner"
		for elem in grab.css_list(css_path):
			row = {}
			for childelems in elem.iterchildren():
				if 'b-serp-item__price' == childelems.attrib['class']:
					row['price'] = find_node_number(childelems, ignore_spaces=True)
				if 'b-serp-item__header' == childelems.attrib['class']:
					row['header'] = get_node_text(childelems)
					ahref = childelems.iterchildren()
					row['link'] = list(ahref)[0].get('href')
				if 'b-serp-item__about' == childelems.attrib['class']:
					row['about'] = get_node_text(childelems)
				if 'b-serp-item__address' == childelems.attrib['class']:
					adresselems = childelems.iterchildren()
					adress_and_subway = list(adresselems)[1]
					adress = adress_and_subway.text
					adress_and_subway_iter = adress_and_subway.iterchildren()
					subway = list(adress_and_subway_iter)[0].text
					row['adress'] = adress
					row['subway'] = subway
				if 'b-serp-item__owner' == childelems.attrib['class']:
					row['onwer']=get_node_text(childelems)
			row['time'] = int(time.time())

			self.csvfilesaver.save(row)
			#dump(obj=row, fp=self.jsonfile, ensure_ascii=False)

if __name__ == '__main__':
	default_logging(grab_log='/tmp/grab.log', level=logging.DEBUG, mode='a',propagate_network_logger=False,network_log='/tmp/grab.network.log')
	bot = YarSpider()
	bot.run()
