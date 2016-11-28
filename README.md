# BinaryToImage

Convert executable binary file into RGB or Greyscale png image format. Repsent 8 bit binary values as pixel and create image from these. It convert one file or multiple files in a directory.

### Options :
   <p> -a		: Both of Greyscale and RGB </p>
   <p> -G		: Greyscale format </p>
   <p> -RGB	: RedGreenBlue format </p>
   <p> -d		: Directory name </p>

#### Sample usage :
 <p> binary2image.py -a sample.exe
 <p> binary2image.py -d /home/user/dir -RGB
 <p> binary2image.py -d /home/user/dir -G
 <p> binary2image.py -d /home/user/dir -a
