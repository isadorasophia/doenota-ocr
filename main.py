import base64

from scripts.DB import *
from scripts.extractData import *
from scripts.ocr import *
from scripts.imgProcess.process import *

rawFolder = "./assets/raw/"
processedFolder = "./assets/processed/"
resultsFolder = "./assets/results/"

extension = ".jpg"

class ReceiptModel():
	def __init__(self):
		pass

	# saves the raw receipt to further use
	def saveReceipt (self):
		rawPath = rawFolder + self.data_id + extension

		with open(rawPath, "wb") as f:
			f.write(base64.decodestring(self.image))
			f.close()

if __name__ == "__main__":
    database = DBop()

    # build your initial data
    receipt = ReceiptModel()
    receipt.data_id, receipt.image = database.getNextImage()

	# saves the image
	# receipt.saveReceipt()

	processor = Processor(rawFolder, processedFolder, receipt.data_id, extension)
	processor.CRSB()
	processor.CTS()

	