#!/usr/bin/python
import os
import sys
import numpy as np

import sFunc
import contour.contourFinder
import skew

if len(sys.argv) > 1:
  inputF = sys.argv[1] # for drawing purposes
else:
  print ('No input image given! \n')

baseName =  os.path.basename(inputF)
image = baseName[:baseName.index(".")]
_, extension = os.path.splitext(inputF)

# set the path
path = './assets/notas-binarized/'

# set output for both final image and its rotated version
output = os.path.join(path, image + 'O' + extension)
outputR = os.path.join(path, image + 'OR' + extension)

# now, get the cropped image
cropped = contour.contourFinder.cropReceipt(inputF)

# check if cropping was successful 
if cropped == None:
	# print('Couldn\'t find borders for the image...')

	# eliminate rotation of the raw image
	skew.process(inputF, output);
else:
	# saves it
	sFunc.save(output, cropped)

	# eliminate rotation
	skew.process(output, output);

# now open it and applies the sauvola threshold
image = sFunc.open(output)

grey = sFunc.greyscale(image)
blurred = sFunc.blur(grey)
binary = sFunc.binarize(blurred, 15)

# save it
sFunc.save(output, binary)

# now, rotate 180 degrees
skew.rotate180(output, outputR)