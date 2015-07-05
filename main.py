import base64
import os

from scripts.DB import *
from scripts.extractData import *
from scripts.ocr import *
from scripts.imgProcess.process import *

rawDir = "./assets/raw/"
processedDir = "./assets/processed/"
resultsDir = "./assets/results/"

extension = ".jpg"

class ReceiptModel():
	def __init__(self):
		pass

	# saves the raw receipt to further use
	def saveReceipt (self):
		rawPath = rawDir + self.data_id + extension

		with open(rawPath, "wb") as f:
			f.write(base64.decodestring(self.image))
			f.close()

	@staticmethod
	def createWorkspace():
		if not os.path.exists(rawDir):
	    	os.makedirs(rawDir)

		if not os.path.exists(processedDir):
	    	os.makedirs(processedDir)

		if not os.path.exists(resultsDir):
	    	os.makedirs(resultsDir)

if __name__ == "__main__":
	createWorkspace()
    database = DBop()

    # build initial data
    receipt = ReceiptModel()
    receipt.data_id, receipt.image = database.getNextImage()

	# saves the image
	# receipt.saveReceipt()

	# process receipt with the respective algorithms
	processor = Processor(rawDir, processedDir, receipt.data_id, extension)
	processor.CRSB()
	processor.CTS()

	# perform ocr on the processed images
	ocr = OCR(processedDir)
	ocr.performOCR(resultsDir)