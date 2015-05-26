import cv2
import os
import Image

cimport numpy as np
import numpy as np
from numpy import linalg

# in order to build: rm -r ./build; rm sFunc.c sFunc.so; python setup.py build_ext -i

# Opens an image with the specified path
# Returns a numpy-array
def open(char *path):
	cdef np.ndarray[np.uint8_t, ndim=3] img = cv2.imread(path)
	return img

# Blurs the image with gaussianBlur
def blur(np.ndarray[double, ndim=2] image):
	cdef np.ndarray[double, ndim=2] img = np.double(cv2.GaussianBlur(image, (5, 5), 0))
	return img

# Returns a greyscaled version of the given image
def greyscale(np.ndarray[np.uint8_t, ndim=3] image):
	cdef np.ndarray[double, ndim=2] img = np.mean(image, axis=2)
	return img

# Saves the given image(numpy-array) into path
def save(char *path, image):
	cv2.imwrite(path, image)

# Blurs the image with gaussianBlur
def binarize(np.ndarray[double, ndim=2] image, int size=15):
	cdef np.ndarray[double, ndim=2] tmp0, tmp1, tmp2, va, vb, binary
	cdef int oldSize, y, x
	cdef double my, i, o, k, t

	tmp0 = np.cumsum(image, axis=1)
	va = np.cumsum(tmp0, axis=0)
	tmp1=image**2
	tmp2 = np.cumsum(tmp1, axis=1)
	vb = np.cumsum(tmp2, axis=0)
	binary = np.zeros((image.shape[0], image.shape[1]))

	oldSize = size

	y = 0
	for row in image:
		x = 0
		for pixel in row:
			if ((y < size) | (x < size)):
				size = min(x,y)

			if (size > 0):
				my = float((va[y][x]-va[y-size][x]-va[y][x-size]+va[y-size][x-size])/size**2)
				i = float(((vb[y,x]-vb[y-size,x]-vb[y,x-size]+vb[y-size,x-size])/size**2)-(my**2))
				if (i < 0):
					i = 0
				o = np.sqrt(i)
				k = 0.1
				t = my * ( 1 + k * ( (o/128) - 1 ) )
				if image [y][x] >= t:
					binary[y][x] = 255
				else:
					binary[y][x] = 0

			size = oldSize
			x = x+1
		y = y+1
		

	return binary