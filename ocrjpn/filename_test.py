  # -*- coding: utf-8 -*-
import os

PATH = "../templates/test/"

def create_list_of_unicode_strings():
    global PATH
    list_of_files = os.listdir(PATH)

    for img in list_of_files:
        print "u\'"+img.split(".bmp")[0]+"\',",

def print_kanji_from_filenames():
    global PATH
    list_of_files = os.listdir(PATH)

    for f in list_of_files:
        tokens = f.strip(".bmp")
        print unichr(int(tokens))

def main():
    global PATH

    list_of_files = os.listdir(PATH)

    names = [u'但', u'位', u'低', u'住', u'佐', u'体', u'悩', u'脳', u'願']

    f = open("names.txt")
    lines = f.read()
    f.close()

    assert len(names) == len(list_of_files)

    for i in range(len(names)):
        os.rename( PATH+list_of_files[i], PATH+str(ord(names[i])) + ".bmp" )
        # print str(ord(names[i])) + ".bmp"

if __name__ == "__main__":
    # create_list_of_unicode_strings()
    print_kanji_from_filenames()