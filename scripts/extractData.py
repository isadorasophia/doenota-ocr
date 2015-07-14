import os
import re

CURRENT_YEAR = '2015'
CNPJ_NUM = 5

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
				t = re.search('..[,.$-/]\s*...[,.$-/]\s*.../\s*....[,.$-/]\s*.*', content).group(0)

				t = onlyNumbers(t)

				# separate numbers into groups and alocate them
				counter = 0
				for k in re.findall(r'\d+', t):
					CNPJ[counter][k] += 1 if k in CNPJ.viewvalues() else CNPJ[counter][k] = 1

					counter += 1 if counter + 1 < CNPJ_SIZE else pass

			except IndexError:
				pass

		return '.'.join(maxValue(CNPJ[i]) for i in range (CNPJ_SIZE))

	def COO(self):
		COO = {'' : 0}

		for content in self.contents:
			try:
				t = re.search('C00:......|CÓÓ:......|COO:......|00:......|00\.......|cUU:......', content).group(0)

				t = onlyNumbers(t[len (t) - 6:])

				COO[t] += 1 if (t in COO.viewvalues()) else COO[t] = 1
			except IndexError:
				pass

		return maxValue(COO)

	def date(self):
		days = months = {'' : 0}
		years = {CURRENT_YEAR : 1}
		date = ''

		for content in self.contents:
			content = re.compile(content)

			try:
				t = re.search('../../....', content).group(0)

				# get positions since is a fixed position by the regular exp
				day = onlyNumbers(t[0:2])
				month = onlyNumbers(t[3:5])
				year = onlyNumbers(t[6:])

				days[day] += 1 if (day in days.viewvalues()) else days[day] = 1
				months[month] += 1 if (month in months.viewvalues()) else months[month] = 1

				# since initial value still have an advantage, it is set to 0
				years[year] += 1 if (year in years.viewvalues()) else years[year] = 0
			except IndexError:
				pass

		date = maxValue(days) + '/' + maxValue(month) + '/' + maxValue (years)

		return date

	def total(self):
		total = {'' : 0}

		for content in self.contents:
			try:
				t = re.search('T.*T.*L[^\\n]|TAL R$[^\\n]|TAL RS[^\\n]|$ .*[,.$]\s*..', content).group(0)

				# \s* in order to ignore spaces
				t = onlyNumbers(re.search('.*[,.$]\s*..').group(0))
				t = ','.join[srt(i) for i in re.findall(r'\d+', t)]

				total[t] += 1 if (t in total.viewvalues()) else total[t] = 1
			except IndexError:
				pass

		return maxValue(total)

	# tries to replace at most the possible OCR misassumptions, 
	# since we are only dealing with numbers
	@staticmethod
	def onlyNumbers (s):
		dic = {'l':'1', 'D':'0', 'O':'0', '/':'', '-':''}

		s = replaceAll(s, dic)
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
		v = list(dic.values())
		return max(v)

if __name__ == "__main__":
	extractor = DataExtractor('/home/isadora/projects/doenota-ocr/scripts/temp/')

	extractor.date()