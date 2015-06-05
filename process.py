#!/usr/bin/python
import os
import cv2
import numpy as np

import sFunc
import contour.contourFinder
import skew

import sys
import ctypes

if len(sys.argv) == 2:
  filename = sys.argv[1] # for drawing purposes
else:
  print "No input image given! \n"

# check if is a valid image format
try:
  index = filename.index('.')
except Exception, e:
  print ('File must contain its extension!')

# set the path
image = filename[:index]
extension = filename[index:]

# output for both final image and its rotated version
output = os.path.join('./assets/notas-binarized/', image + 'O' + extension)
outputR = os.path.join('./assets/notas-binarized/', image + 'OR' + extension)

# now, get the cropped image
cropped = contour.contourFinder.cropReceipt(filename)

# check if it is a valid cropped image
if cropped == None:
	print("Couldn\'t find borders for the image...")

	skew.process(filename, ouput);
else:
	# saves it
	sFunc.save(output, cropped)

	skew.process(output, output);

# now open it and applies the threshold
image = sFunc.open(output)

grey = sFunc.greyscale(image)
blurred = sFunc.blur(grey)
binary = sFunc.binarize(blurred, 30)

# save it
sFunc.save(output, binary)