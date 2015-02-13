__author__ = 'RKazakov'

from .. import saver
import codecs
import csv
import cStringIO

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    https://docs.python.org/2.7/library/csv.html
    """
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class CsvRowSaver(saver.RowSaver):
	"""
	Save Unicode strong to csv file
	"""
	def __init__(self, csvfilename, fieldnames, dicname='YarDic'):
		self.dicname = dicname
		self.fieldnames = fieldnames
		self.csvfile = open(csvfilename, 'w')
		self.dic_writer = UnicodeWriter(self.csvfile, dialect=self.dicname)
		self.dic_writer.writerow(self.fieldnames)
		saver.RowSaver.__init__(self)

	def save(self, row):
		self.dic_writer.writerow(row)