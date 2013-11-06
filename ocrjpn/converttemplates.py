  # -*- coding: utf-8 -*-
from PIL import Image
import os
from imagetests import threshold_image, save_image

def open_threshold_save(im, save_name):
    new_image = threshold_image(im)
    save_image(new_image, save_name, "BMP")

def crop_to_whitespace(im):
    #this is a tuple
    im_x, im_y = im.size

    pixel_vals = []

    #two-dimensional array of the pixels (but like really this is probably not the way to do things)
    for i in range(im_y):
        l = []
        for j in range (im_x):
            l.append(im.getpixel((j,i)))
        pixel_vals.append( l )

    #umm okay yeah so if the ENTIRE ROW is white, we need that info

    nonwhiterows = []

    for i in range(len(pixel_vals)):
        for j in range(len(pixel_vals[i])):
            if pixel_vals[i][j] < 172:
                nonwhiterows.append((j,i))
                im.putpixel( (j,i), (0) )
            else:
                im.putpixel( (j,i), (255) )

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

    region = im.crop(box)

    return region

def make_templates(im, kanji):
    width = 200 #125 for kanji
    height = 150 #145 for kanji
    origin = 0
    box = (0, 0, width, height)
    row = 1

    for i in range(1, len(kanji)+1):
        print i
        print box
        work = im.crop(box)
        new_work = crop_to_whitespace(work)
        open_threshold_save(new_work, kanji[i-1]+".bmp")

        if i % 5 == 0 and i != 0: #8 for kanji
            #go to the next line
            box = (origin, origin + (row*height), width, height*(row+1))
            row += 1
        else:
            box = (box[0]+width, box[1], box[2]+width, box[3])

def main():

    raw_dir = "../idk/original mincho files/hiragana"

    num_chars = 35 #for kanji templates, 64

    list_of_files = os.listdir(raw_dir) 
    raw_kanji = u"あ　い　う　え　お か　き　く　け　こ さ　し　す　せ　そ た　ち　つ　て　と な　に　ぬ　ね　の は　ひ　ふ　へ　ほ ま　み　む　め　も ら　り　る　れ　ろ わ　を　ん　が　ぎ ぐ　げ　ご　ざ　じ　ず　ぜ　ぞ　だ　ぢ　づ　で　ど　ば　び　ぶ　べ　ぼ　ぱ　ぴ　ぷ　ぺ　ぽ　や　ゆ　よ　ゐ　ゑ"
    kanji = raw_kanji.split()
    start = 0
    end = num_chars

    kanji_template_box = (125,145,1145,1305)
    kana_template_box = (95,148,1095,1198)

    print len(kanji)

    for f in list_of_files:

        im = Image.open(raw_dir+"/"+f).convert("L")

        cropped = im.crop(kana_template_box)
        make_templates(cropped, kanji[start:end])
        start += num_chars
        end += num_chars

if __name__ == "__main__":
    main()