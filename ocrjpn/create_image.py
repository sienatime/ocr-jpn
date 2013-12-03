from PIL import Image
import re
import cStringIO
import recognize
import pdb

def img_from_string(imgdata, coords):
    imgstr = re.search(r'base64,(.*)', imgdata).group(1)

    lbox = []
    for val in coords:
        lbox.append( clean_coords(val) )

    box = tuple(lbox)
    tempimg = cStringIO.StringIO(imgstr.decode('base64'))

    im = Image.open(tempimg)
    cropped = im.crop(box)

    return recognize.ocr_image(cropped)

def clean_coords(number):
    #these come in as unicode strings, for some reason. need to round and make them ints.
    floated = float(number)
    base = int(floated)
    if floated % base >= 0.5:
        return base + 1
    else:
        return base

def main():
    imgdata = (open("imgdata.txt").read())
    print img_from_string(imgdata)

if __name__ == "__main__":
    main()