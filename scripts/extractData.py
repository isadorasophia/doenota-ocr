#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

CURRENT_YEAR = '2015'
CNPJ_SIZE = 5

class DataExtractor():
	def __init__(self, path):
		files = [path + f for f in os.listdir(path)]

		self.contents = []

		for f in files:
			with open(f, 'r') as txt:
				self.contents += [txt.read()]

	def CNPJ(self):
		CNPJ = [{'' : 0} for k in range(CNPJ_SIZE)]

		for content in self.contents:
			try:
				content = re.sub(r'(..)[,.$-/]\s*(...)[,.$-/]\s*(...)[./]\s*(....)[,.$-/]\s*(..)', r'\1.\2.\3.\4.\5', content)
				t = re.search('..[,.$-/]\s*...[,.$-/]\s*...[./]\s*....[,.$-/]\s*..', content).group(0)

				t = DataExtractor.onlyNumbers(t)

				# separate numbers into groups and alocate them
				counter = 0
				for k in re.findall(r'\d+', t):
					if k in CNPJ[counter].keys():
						CNPJ[counter][k] += DataExtractor.accuracy(k)
					else:
						CNPJ[counter][k] = DataExtractor.accuracy(k)

					if counter + 1 < CNPJ_SIZE:
						counter += 1
					else:
						break
			except AttributeError, IndexError:
				pass

		return ''.join(DataExtractor.maxValue(CNPJ[i]) for i in range (CNPJ_SIZE))

	def COO(self):
		COO = {'' : 0}

		for content in self.contents:
			try:
				t = re.search('C00[:,./]......|CÓÓ:......|COO:......|00:......|00\.......|cUU:......', content).group(0)

				t = DataExtractor.onlyNumbers(t[len (t) - 6:])

				if t in COO.keys():
					COO[t] += DataExtractor.accuracy(t)
				else:
					COO[t] = DataExtractor.accuracy(t)
			except AttributeError, IndexError:
				pass

		return DataExtractor.maxValue(COO)

	def date(self):
		days = {'' : 0}
		months = {'' : 0}
		years = {CURRENT_YEAR : 1}
		date = ''

		for content in self.contents:
			try:
				t = re.search('../../....', content).group(0)

				# get positions since is a fixed position by the regular exp
				day = DataExtractor.onlyNumbers(t[0:2])
				month = DataExtractor.onlyNumbers(t[3:5])
				year = DataExtractor.onlyNumbers(t[6:])

				if day in days.keys():
					days[day] += DataExtractor.accuracy(day)
				else:
					days[day] = DataExtractor.accuracy(day)

				if month in months.keys():
					months[month] += DataExtractor.accuracy(month)
				else: 
					months[month] = DataExtractor.accuracy(month)

				# since initial value still have an advantage, it is set to 0
				if year in years.keys():
					years[year] += 1
				else:
					years[year] = 0
			except AttributeError, IndexError:
				pass

		date = DataExtractor.maxValue(days) + '/' + DataExtractor.maxValue(months) + '/' + DataExtractor.maxValue(years)

		return date

	def total(self):
		total = {'' : 0}

		for content in self.contents:
			try:
				t = re.search(r'T.T.L ([A-Za-z\d .]+)|TAL R$ ([A-Za-z\d .]+)|T.L RS ([A-Za-z\d .]+)|T.L Rs ([A-Za-z\d .]+)|$ .*[,.$]\s*..', content).group(0)

				# \s* in order to ignore spaces
				t = DataExtractor.onlyNumbers(t)
				t = re.search(r'\d+[,$/. ]+..', t).group(0)

				t = ','.join(re.findall(r'\d+', t))
 
				if t in total.keys(): 
					total[t] += DataExtractor.accuracy(t)
				else:
					total[t] = DataExtractor.accuracy(t)
			except AttributeError, IndexError:
				pass

		return DataExtractor.maxValue(total)

	# tries to replace at most the possible OCR misassumptions, 
	# since we are only dealing with numbers
	@staticmethod
	def onlyNumbers (s):
		dic = {'l':'1', 'D':'0', 'B':'8', 'I':'1', 'O':'0', 'o':'0', '/':'', '-':''}

		s = DataExtractor.replaceAll(s, dic)
		return s

	# replace all occurrences of a key with its value
	@staticmethod
	def replaceAll (s, dic):
		for i, j in dic.iteritems():
			s = s.replace(i, j)

		return s

	# returns max value in a dict
	@staticmethod
	def maxValue (dic):
		k = list(dic.keys())
		v = list(dic.values())

		return k[v.index(max(v))]

	@staticmethod
	def accuracy(s):
		if s.isdigit():
			return 2
		else:
			return 1

if __name__ == "__main__":
	# testing script
	# extractor = DataExtractor('./temp/')

	# print extractor.date()