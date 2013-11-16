from PIL import Image
import re
import cStringIO

def img_from_string(imgdata):
    imgstr = re.search(r'base64,(.*)', imgdata).group(1)

    output = open('output.jpeg', 'wb')

    output.write(imgstr.decode('base64'))

    output.close()

    tempimg = cStringIO.StringIO(imgstr.decode('base64'))

    im = Image.open(tempimg)
    im.show()

def main():
    imgdata = (open("imgdata.txt").read())
    img_from_string(imgdata)

if __name__ == "__main__":
    main()