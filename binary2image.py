# Binary to Image Converter
# Read executable binary files and convert them RGB and greyscale png images
#
# Author: Necmettin Çarkacı
# E-mail: necmettin [ . ] carkaci [ @ ] gmail [ . ] com

import os, math
import argparse
from PIL import Image
from queue import Queue
from threading import Thread


def getBinaryData(filename):
	"""
	Extract byte values from binary executable file and store them into list
	:param filename: executable file name
	:return: byte value list
	"""

	binary_values = []

	with open(filename, 'rb') as fileobject:

		# read file byte by byte
		data = fileobject.read(1)

		while data != b'':
			binary_values.append(ord(data))
			data = fileobject.read(1)

	return binary_values


def createGreyScaleImage(filename, width=None):
	"""
	Create greyscale image from binary data. Use given with if defined or create square size image from binary data.
	:param filename: image filename
	"""
	greyscale_data  = getBinaryData(filename)
	size            = get_size(len(greyscale_data), width)
	save_file(filename, greyscale_data, size, 'L')


def createRGBImage(filename, width=None):
	"""
	Create RGB image from 24 bit binary data 8bit Red, 8 bit Green, 8bit Blue
	:param filename: image filename
	"""
	index = 0
	rgb_data = []

	# Read binary file
	binary_data = getBinaryData(filename)

	# Create R,G,B pixels
	while (index + 3) < len(binary_data):
		R = binary_data[index]
		G = binary_data[index+1]
		B = binary_data[index+2]
		index += 3
		rgb_data.append((R, G, B))

	size = get_size(len(rgb_data), width)
	save_file(filename, rgb_data, size, 'RGB')


def save_file(filename, data, size, image_type):

	try:
		image = Image.new(image_type, size)
		image.putdata(data)

		# setup output filename
		dirname     = os.path.dirname(filename)
		name, _     = os.path.splitext(filename)
		name        = os.path.basename(name)
		imagename   = dirname + os.sep + image_type + os.sep + name + '_'+image_type+ '.png'
		os.makedirs(os.path.dirname(imagename), exist_ok=True)

		image.save(imagename)
		print('The file', imagename, 'saved.')
	except Exception as err:
		print(err)


def get_size(data_length, width=None):
	# source Malware images: visualization and automatic classification by L. Nataraj
	# url : http://dl.acm.org/citation.cfm?id=2016908

	if width is None: # with don't specified any with value

		size = data_length

		if (size < 10240):
			width = 32
		elif (10240 <= size <= 10240 * 3):
			width = 64
		elif (10240 * 3 <= size <= 10240 * 6):
			width = 128
		elif (10240 * 6 <= size <= 10240 * 10):
			width = 256
		elif (10240 * 10 <= size <= 10240 * 20):
			width = 384
		elif (10240 * 20 <= size <= 10240 * 50):
			width = 512
		elif (10240 * 50 <= size <= 10240 * 100):
			width = 768
		else:
			width = 1024

		height = int(size / width) + 1

	else:
		width  = int(math.sqrt(data_length)) + 1
		height = width

	return (width, height)


def run(file_queue, width):

	while not file_queue.empty():
		filename = file_queue.get()
		createGreyScaleImage(filename, width)
		createRGBImage(filename, width)
		file_queue.task_done()


def main(input_dir, width=None, thread_number=7):

	# Get all executable files in input directory and add them into queue
	file_queue = Queue()
	for root, directories, files in os.walk(input_dir):
		for filename in files:
			file_path = os.path.join(root, filename)
			file_queue.put(file_path)

	# Start thread
	for index in range(thread_number):
		thread = Thread(target=run, args=(file_queue, width))
		thread.daemon = True
		thread.start()
	file_queue.join()


if __name__ == '__main__':

	parser = argparse.ArgumentParser(prog='binar2image.py', description="Convert binary file to image")
	parser.add_argument(dest='input_dir', help='Input directory path is which include executable files')

	args = parser.parse_args()

	main(args.input_dir, width=None)

