import os
import subprocess

class OCR():
	def __init__(self, path):
		self.files = [path + f for f in os.listdir(path)]

		# by default, free to change it
		self.lang = ['not', 'not2']

	def performOCR(self, path):
		# follows generated output
		output = 1

		for img in self.files:
			for lang in self.lang:
				command = ['tesseract', img, path + str(output), '-l', lang]

				# execute tesseract
				process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

				process.wait()

				# if op was a success...
				if os.path.isfile(path + str(output) + '.txt'):
					output += 1