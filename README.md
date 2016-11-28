# BinaryToImage

Convert executable binary file into RGB or Greyscale png image format. Repsent 8 bit binary values as pixel and create image from these. It convert one file or multiple files in a directory.

Options :
	-a		: Both of Greyscale and RGB 
	-G		: Greyscale format
	-RGB	: RedGreenBlue format
	-d		: Directory name

Sample usage :
	binary2image.py -a sample.exe
	binary2image.py -d /home/user/dir -RGB
	binary2image.py -d /home/user/dir -G
	binary2image.py -d /home/user/dir -a
