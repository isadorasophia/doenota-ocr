import numpy as np

from contour import contourFinder
import sFunc
import skew
import cropText

class Processor():
	def __init__(self, rawFolder, processedFolder, data_id, extension):
		self.rawPath = rawPath
		self.processedFolder = processedFolder

		self.name = data_id
		self.extension = extension

		self.outputs = 1

	def output(self):
		output = self.rawPath + self.name + self.outputs + self.extension
		self.outputs += 1

		return output

	# stands for Crop Receipt, Skew and Binarize
	def CRSB(self):
		_input = self.rawPath + self.name + self.extension

		# first, get the cropped image
		cropped = contourFinder.cropReceipt(_input)

		curOutput = self.output()

		# check if cropping was successful 
		if cropped == None:
			# just eliminate rotation of raw image
			skew.process(_input, curOutput)

		else:
			# saves it
			sFunc.save(curOutput, cropped)

			# eliminate rotation
			skew.process(curOutput, curOutput)

		# now open the image and applies the sauvola threshold
		image = sFunc.open(curOutput)

		grey = sFunc.greyscale(image)
		blurred = sFunc.blur(grey)
		binary = sFunc.binarize(blurred, 15)

		# save it
		sFunc.save(curOutput, binary)

		# finally, rotate 180 degrees in a new output
		skew.rotate180(curOutput, self.output())

	# stands for Crop Text and Skew
	def CTS(self):
		_input = self.rawPath + self.name + self.extension

		curOutput = self.output()

		cropText.mainTextDetection(_input, curOutput)
		skew.process(curOutput, curOutput)
		skew.rotate180(curOutput, self.output())