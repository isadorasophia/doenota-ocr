#!/usr/bin/python
import os
import cv2
import numpy as np

import sFunc
import contour.contourFinder

import sys
import ctypes

if len(sys.argv) == 2:
  filename = sys.argv[1] # for drawing purposes
else:
  print "No input image given! \n"

try:
  index = filename.index('.')
except Exception, e:
  print ('File must contain its extension!')

image = filename[:index]
extension = filename[index:]
output = os.path.join('./', image + '-output' + extension)

# gets the cropped image
cropped = contour.contourFinder.cropReceipt(filename)

# saves it
sFunc.save(output, cropped)

# now open it and applies the threshold
image = sFunc.open(output)

grey = sFunc.greyscale(image)
blurred = sFunc.blur(grey)
binary = sFunc.binarize(blurred, 75)

# save it
sFunc.save(output, binary)
