import base64
import os
import shutil

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
	def saveReceipt (self, idDir):
		rawPath = rawDir + idDir + self.data_id + extension

		with open(rawPath, "wb") as f:
			f.write(base64.decodestring(self.image))
			f.close()

	@staticmethod
	def createWorkspace(idDir):
		if not os.path.exists(rawDir):
	    	os.makedirs(rawDir + idDir)

		if not os.path.exists(processedDir):
	    	os.makedirs(processedDir + idDir)

		if not os.path.exists(resultsDir):
	    	os.makedirs(resultsDir + idDir)

	@staticmethod
	def cleanWorkspace(idDir):
		shutil.rmtree(rawDir + idDir)
		shutil.rmtree(processedDir + idDir)
		shutil.rmtree(resultsDir + idDir)

if __name__ == "__main__":
    database = DBop()

    # build initial data
    receipt = ReceiptModel()
    receipt.data_id, receipt.image = database.getNextImage()

    # local directory for data handling
    idDir = receipt.data_id + '/'

    createWorkspace(idDir)

	# saves the image
	# receipt.saveReceipt(idDir)

	# process receipt with the respective algorithms
	processor = Processor(rawDir + idDir, processedDir + idDir, receipt.data_id, extension)
	processor.CRSB()
	processor.CTS()

	# perform ocr on the processed images
	ocr = OCR(processedDir + idDir)
	ocr.performOCR(resultsDir + idDir)

	extractor = DataExtractor(resultsDir + idDir)

	# perform data extract
	receipt.COO = extractor.COO()
	receipt.CNPJ = extractor.CNPJ()
	receipt.date = extractor.date()
	receipt.total = extractor.total()

	database.save(receipt.data_id, receipt.CNPJ, receipt.date, receipt.COO, 
		receipt.total)

	receipt.cleanWorkspace(idDir)