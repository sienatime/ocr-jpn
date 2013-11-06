  # -*- coding: utf-8 -*-
from PIL import Image
# import code
from sys import argv

script, img = argv

def open_threshold_save(im_name, save_name):
    im = Image.open(im_name).convert("L")
    new_image = threshold_image(im)
    save_image(new_image, save_name, "BMP")
    new_image.show()

def threshold_image(im):
    #this is a tuple
    im_x, im_y = im.size

    pixel_vals = []

    #two-dimensional array of the pixels (but like really this is probably not the way to do things)
    for i in range(im_y):
        l = []
        for j in range (im_x):
            l.append(im.getpixel((j,i)))
        pixel_vals.append( l )

    for i in range(len(pixel_vals)):
        for j in range(len(pixel_vals[i])):
            if pixel_vals[i][j] < 172:
                im.putpixel( (j,i), (0) )
            else:
                im.putpixel( (j,i), (255) )

    return im

def save_image(im, filename, filetype):
    im.save(filename, filetype)

def resize_and_crop_image(im):
    if im.size[0] > 128:
        size = 128, 128
        #if we don't resize the image, it's like, a lot of pixels to deal with...
        im.thumbnail(size)

    out = im.point(lambda i: i * 2)

    #this is a tuple
    im_x, im_y = im.size

    pixel_vals = []

    #two-dimensional array of the pixels (but like really this is probably not the way to do things)
    for i in range(im_y):
        l = []
        for j in range (im_x):
            l.append(out.getpixel((j,i)))
        pixel_vals.append( l )

    #umm okay yeah so if the ENTIRE ROW is white, we need that info

    nonwhiterows = []

    for i in range(len(pixel_vals)):
        for j in range(len(pixel_vals[i])):
            if pixel_vals[i][j] < 172:
                nonwhiterows.append((j,i))
                out.putpixel( (j,i), (0) )
            else:
                out.putpixel( (j,i), (255) )

    #so now that I have a list of nonwhite rows, I need to find the extreme x AND y values. so I probably need a list of coordinates anyway. and then i can compare the coordinates to each other. so i should probably have a list of tuples or something.

    upper = nonwhiterows[0][1]
    lower = nonwhiterows[-1][1]

    min_x = im_x
    max_x = 0

    for x, y in nonwhiterows:
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x

    box = (min_x, upper, max_x+1, lower+1)

    region = out.crop(box)

    return region

def compare_to_template(im, template):
    im = im.resize(template.size)
    im_x, im_y = im.size
    tmp_x, tmp_y = template.size

    # TODO instead of getpixel of every coord, use list(im.getdata()) (or just im.getdata() which is a PIL object)

    im_pixel_vals = []
    #two-dimensional array of the pixels (but like really this is probably not the way to do things)
    for i in range(im_y):
        for j in range(im_x):
            im_pixel_vals.append(im.getpixel((j,i)))

    tmp_pixel_vals = []

    for i in range(tmp_y):
        for j in range(tmp_x):
            tmp_pixel_vals.append(template.getpixel((j,i)))

    differences = [ int(abs((tmp_pixel_vals[i] - im_pixel_vals[i]))/255) for i in range(len(im_pixel_vals)) ]

    total = sum(differences)

    # code.interact(local=locals())

    return float(total)/(im_x * im_y)

def main():
    #from argv use img
    im = Image.open(img).convert("L")
    new_image = resize_and_crop_image(im)

    templates = [
        (u"朝","templates/asat.bmp"),(u"あ","templates/printat.bmp"),(u"お","templates/printot.bmp")
        ]

    scores = []

    for char, filename in templates:
        template = Image.open(filename).convert("L")
        scores.append( (char, filename, compare_to_template(new_image, template)) )

    most_similar = scores[0]
    print scores

    for i in range(1, len(scores) ):
        if scores[i][2] < most_similar[2]:
            most_similar = scores[i]

    print "The image was most similar to ", most_similar[0]

if __name__ == "__main__":
    main()