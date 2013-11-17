from PIL import Image
import re
import cStringIO

def img_from_string(imgdata, coords):
    imgstr = re.search(r'base64,(.*)', imgdata).group(1)

    print coords

    lbox = []
    for val in coords:
        lbox.append( int(float(val)) )

    box = tuple(lbox)

    tempimg = cStringIO.StringIO(imgstr.decode('base64'))

    im = Image.open(tempimg)
    cropped = im.crop(box)
    cropped.show()

def main():
    imgdata = (open("imgdata.txt").read())
    img_from_string(imgdata)

if __name__ == "__main__":
    main()