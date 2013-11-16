from PIL import Image
import re
import cStringIO

imgdata = (open("imgdata.txt").read())

imgstr = re.search(r'base64,(.*)', imgdata).group(1)

output = open('output.jpeg', 'wb')

output.write(imgstr.decode('base64'))

output.close()

tempimg = cStringIO.StringIO(imgstr.decode('base64'))

im = Image.open(tempimg)
im.show()