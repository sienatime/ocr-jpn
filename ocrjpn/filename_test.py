  # -*- coding: utf-8 -*-
import os

PATH = "../templates/katakana/mincho/"

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

    names = [u'ア', u'イ', u'ウ', u'エ', u'オ', u'カ', u'ガ', u'キ', u'ギ', u'ク', u'グ', u'ケ', u'ゲ', u'コ', u'ゴ', u'サ', u'ザ', u'シ', u'ジ', u'ス', u'ズ', u'セ', u'ゼ', u'ソ', u'ゾ', u'タ', u'ダ', u'チ', u'ヂ', u'ツ', u'ヅ', u'テ', u'デ', u'ト', u'ド', u'ナ', u'ニ', u'ヌ', u'ネ', u'ノ', u'ハ', u'バ', u'パ', u'ヒ', u'ビ', u'ピ', u'フ', u'ブ', u'プ', u'ヘ', u'ベ', u'ペ', u'ホ', u'ボ', u'ポ', u'マ', u'ミ', u'ム', u'メ', u'モ', u'ヤ', u'ユ', u'ヨ', u'ラ', u'リ', u'ル', u'レ', u'ロ', u'ワ', u'ヰ', u'ヱ', u'ヲ', u'ン']

    assert len(names) == len(list_of_files)

    for i in range(len(names)):
        os.rename( PATH+list_of_files[i], PATH+str(ord(names[i])) + ".bmp" )
        # print str(ord(names[i])) + ".bmp"

if __name__ == "__main__":
    # create_list_of_unicode_strings()
    main()