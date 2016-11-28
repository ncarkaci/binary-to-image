#!/usr/bin/env python
#
# Binary to Image Converter
# Read executable binary files and convert them RGB and greyscale png images
#
# Author: Necmettin Çarkacı
# E-mail: necmettin [ . ] carkaci [ @ ] gmail [ . ] com
#
#Usage : binary2image.py /home/user/binaryDir


import sys, os, math, Image

def getBinaryData(filename):
	
	binaryValues = []
	file = open(filename, "rb")
	
	try:
		
    		data = file.read(1) # read byte by byte
		
    		while data != "":
			
        		binaryValues.append(ord(data)) # store value to array	
			data = file.read(1) # get next byte value
			
	finally:
    		file.close()
	
	return binaryValues 

def createGreyScaleImage(dataSet,outputfilename):
	'''
		Create greyscale image from binary data
	'''

	size = int(math.sqrt(len(dataSet)))+1
	image = Image.new('L', (size,size))

	image.putdata(dataSet)

	imagename = outputfilename+"_greyscale.png" 
	image.save(imagename)
	#image.show() 		
	print imagename+" Greyscale image created"

def createRGBDataSet(dataSet):
	index = 0
	resultSet = []
	while ((index+3) < len(dataSet)):
		
		R = dataSet[index]
		index = index+1
		G = dataSet[index]
		index = index+1		
		B = dataSet[index]
		index = index+1	
		resultSet.append((R,G,B))
	return resultSet	

def createRGBImage(rgbData, outputfilename):
	size = int(math.sqrt((len(rgbData))))+1
	image = Image.new( 'RGB', (size,size), "black") # create a new black image
	image.putdata(rgbData)
	
	imagename = outputfilename+"_rgb.png" 
	image.save(imagename)
	#image.show() 		
	print imagename+ " RGB image created"


def getFilepaths(directory):
	''' 
		Collect all files form given directory and return their paths list
	'''

	file_paths = []

	for root, directories, files in os.walk(directory):
		for filename in files:
			filepath = os.path.join(root, filename)
			file_paths.append(filepath) 
	
	return file_paths

def clean(directory, fileExt):
	'''
		delete all files in directory as a given file extension which describe parameter
		
	'''
	for root, directories, files in os.walk(directory):
		for filename in files:
			if filename.endswith(fileExt):
				filepath = os.path.join(root, filename)
				os.remove(filepath)

if __name__ == '__main__':
	
	directory = sys.argv[1]
	filepaths = getFilepaths(directory)
	
	for filename in filepaths:
		print filename	 
		binaryData = getBinaryData(filename)
		createGreyScaleImage(binaryData,filename)
		rgbData    = createRGBDataSet(binaryData)
		createRGBImage(rgbData,filename)

	#clean(sys.argv[1],".png")

