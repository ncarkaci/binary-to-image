#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Binary to Image Converter
# Read executable binary files and convert them RGB and greyscale png images
#
# Author: Necmettin Çarkacı
# E-mail: necmettin [ . ] carkaci [ @ ] gmail [ . ] com
#
#Usage : binary2image.py /home/user/binaryDir outputdir width


import sys, os, math, Image
from Queue import Queue
from threading import Thread, current_thread

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

	imagename = outputfilename+".png" 
	image.save(imagename)
	#image.show() 		
	print imagename+" Greyscale image created"

def createGreyScaleImageSpecificWith(dataSet,outputfilename,width=0):
	'''
		Create greyscale image from binary data
		@ source Malware images: visualization and automatic classification by L. Nataraj
		@ url http://dl.acm.org/citation.cfm?id=2016908
	'''
	if (width == 0): # don't specified
		size = len(dataSet)

		if (size < 10240) :
			width = 32
		elif (10240 <= size <= 10240*3 ):
			width = 64
		elif (10240*3 <= size <= 10240*6 ):
			width = 128	
		elif (10240*6 <= size <= 10240*10 ):
			width = 256
		elif (10240*10 <= size <= 10240*20 ):
			width = 384
		elif (10240*20 <= size <= 10240*50 ):
			width = 512
		elif (10240*50 <= size <= 10240*100 ):
			width = 768
		else :
			width = 1024

	height = int(size/width)+1

	image = Image.new('L', (width,height))

	image.putdata(dataSet)

	imagename = outputfilename+".png" 
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

def run(fileQueue,outDirectory,width):
	while not fileQueue.empty():
		sourceFilename  = fileQueue.get()
		path, name 	= os.path.split(sourceFilename)
		name		= name.split('.')[0]

		outputDir	= os.getcwd()+os.sep+outDirectory+os.sep
		outputFilename	= outputDir+name

		if not os.path.exists(outputDir):
			os.makedirs(outputDir)

		binaryData = getBinaryData(sourceFilename)
		createGreyScaleImageSpecificWith(binaryData,outputFilename,width)
		#createGreyScaleImage(binaryData,outputFilename)
		#rgbData    = createRGBDataSet(binaryData)
		#createRGBImage(rgbData,outputFilename)
		#print (current_thread())
		fileQueue.task_done()


if __name__ == '__main__':

	width 		= 0	
	inputDirectory 	= sys.argv[1]
	outDirectory 	= sys.argv[2]
	width 		= int(sys.argv[3])

	filepaths = getFilepaths(inputDirectory)

	fileQueue = Queue()

	for sourceFilename in filepaths:
		fileQueue.put(sourceFilename)

	for i in range(7):
		t = Thread(target = run, args = (fileQueue,outDirectory,width))
		t.daemon = True
		t.start()

	fileQueue.join()
	#clean(sys.argv[1],".png")

