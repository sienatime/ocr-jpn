from PIL import Image

def resize_and_crop_image(im):
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
            if pixel_vals[i][j] != 255:
                nonwhiterows.append((j,i))
                #once we find the first instance, break (aka exit this loop)

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

def main():
    im = Image.open("a-offset.bmp").convert("L")
    new_image = resize_and_crop_image(im)
    new_image.show()

if __name__ == "__main__":
    main()