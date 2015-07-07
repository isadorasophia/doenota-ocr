import os
import re

class DataExtractor():
	def __init__(self, path):
		files = [path + f for f in os.listdir(path)]

		self.contents = []

		for f in files:
			with open(f, 'r') as txt:
				self.contents += [txt.read()]

	def CNPJ(self):
		return

	def COO(self):
		return

	def date(self):
		dates = []

		for content in self.contents:
			if re.search('../../....', content) != None:
				begin, end = re.search('../../....', content).span()
				
				candidate = content[begin:end]

				day = self.onlyNumbers(candidate[0:2])
				month = self.onlyNumbers(candidate[3:5])
				year = 20 + self.onlyNumbers(candidate[8:])

				candidate = day + "/" + month + "/" + year

				dates += [candidate]

		for candidate in dates

	def total(self):
		return

if __name__ == "__main__":
	extractor = DataExtractor('/home/isadora/projects/doenota-ocr/scripts/temp/')

	extractor.date()