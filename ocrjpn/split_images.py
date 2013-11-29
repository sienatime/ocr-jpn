from PIL import Image
import recognize

def find_split_ranges(l):
    split_ranges = []
    slice_start = 0

    length = len(l)

    for i in range(length):
        if i == length-1 or l[i] + 1 != l[i+1]:
            rng = l[slice_start:i+1]

            # okay let's be real. instead of just blindly accepting things, i need to maybe be like okay, what is the average width/height of the stuff that i just found? are there ones that are significantly less? if there are, i need to either ignore them, or smoosh them back together, which i feel like would be hard. especially since right now i have the blank spaces and not the characters themselves as my points of interest.
            if len(rng) >= 2:
                split_ranges.append( rng )
            slice_start = i+1

    return split_ranges

def find_white_cols(im):
    x, y = im.size
    white_cols = []
    for i in range(x):
        if im.getpixel((i, 0)) == 255:
            for j in range(1, y):
                if im.getpixel(( i, j )) == 0:
                    break
            if j == y - 1:
                white_cols.append(i)
    return white_cols

def find_white_rows(im):
    x, y = im.size
    white_rows = []
    for i in range(y):
        if im.getpixel((0, i)) == 255:
            for j in range(1, x):
                if im.getpixel(( j, i )) == 0:
                    break
            if j == x - 1:
                white_rows.append(i)
    return white_rows

def split_images(im, direction):
    im_x, im_y = im.size
    
    final_images = []
    boxes = []
    start_x = 0
    start_y = 0
    
    #okay so if the direction is WIDE we try to split on the columns. BUT we might run into a problem if there is like, one bar of dark pixels on the bottom, in which case we need to split horiziontally FIRST. but idk yet how i am going to do that.
    if direction == "wide":
        white_cols = find_white_cols(im)
        if len(white_cols) == 0:
            print "didn't find any white columns"
            white_rows = find_white_rows(im)
            print white_rows
        split_ranges = find_split_ranges(white_cols)
        end = im_y

        for rng in split_ranges:
            boxes.append( (start_x, start_y, rng[0], end) )
            start_x = rng[-1] + 1

        try:
            boxes.append( (split_ranges[-1][-1], start_y, im_x, end) )
        except(IndexError):
            print split_ranges
            print "split ranges out of range"



    elif direction == "tall":
        white_rows = find_white_rows(im)
        if len(white_rows) == 0:
            print "didn't find any white rows"
        split_ranges = find_split_ranges(white_rows)
        end = im_x

        for rng in split_ranges:
            boxes.append( (start_x, start_y, end, rng[0]) )
            start_y = rng[-1] + 1
        try:
            boxes.append( ( start_x, split_ranges[-1][-1], end, im_y) )
        except(IndexError):
            print split_ranges
            print "split ranges out of range"


    for box in boxes:
        cropped = im.crop(box)
        new_im = recognize.process_image(cropped)
        final_images.append(new_im)

    return final_images