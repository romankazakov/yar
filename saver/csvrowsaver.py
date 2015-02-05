__author__ = 'RKazakov'

import saver
import codecs
import csv


class CsvRowSaver(saver.RowSaver):

	def __init__(self, csvfilename, fieldnames, dicname='excel'):
		self.dicname = dicname
		self.fieldnames = fieldnames
		self.csvfile = codecs.open(csvfilename, 'w', encoding='UTF-8')
		self.dic_writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames, dialect=self.dicname)
		saver.RowSaver.__init__(self)

	def save(self, row):
		self.dic_writer.writerow(row)