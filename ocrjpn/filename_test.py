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

def codepts_from_chars():
    chars = u"媛 怨 鬱 唄 淫 咽 茨 彙 椅 萎 畏 嵐 宛 顎 曖 挨 韓 鎌 葛 骸 蓋 崖 諧 潰 瓦 牙 苛 俺 臆 岡 旺 艶 稽 憬 詣 熊 窟 串 惧 錦 僅 巾 嗅 臼 畿 亀 伎 玩 挫 沙 痕 頃 駒 傲 乞 喉 梗 虎 股 舷 鍵 拳 桁 隙 呪 腫 嫉 叱 鹿 餌 摯 恣 斬 拶 刹 柵 埼 塞 采 戚 脊 醒 凄 裾 須 腎 芯 尻 拭 憧 蹴 羞 袖 汰 遜 捉 踪 痩 曽 爽 遡 狙 膳 箋 詮 腺 煎 羨 鶴 爪 椎 捗 嘲 貼 酎 緻 綻 旦 誰 戴 堆 唾 鍋 謎 梨 奈 那 丼 貪 頓 栃 瞳 藤 賭 妬 填 溺 諦 阜 訃 肘 膝 眉 斑 阪 汎 氾 箸 剥 罵 捻 虹 匂 喩 闇 弥 冶 麺 冥 蜜 枕 昧 勃 頬 貌 蜂 蔑 璧 餅 蔽 脇 麓 籠 弄 呂 瑠 瞭 侶 慄 璃 藍 辣 拉 沃 瘍 妖 湧 柿 哺 楷 睦 釜 錮 賂 毀 勾"
    char_list = chars.split()

    code_points = []

    for c in char_list:
        code_points.append(ord(c))

    print code_points

    # list_of_files = os.listdir("../templates/kanji/gothic extra")

    # counter = 0
    # for c in code_points:
    #     fmt = str(c) + ".bmp"
    #     if fmt in list_of_files and not os.path.exists("../templates/kanji/gothic/"+fmt):
    #         os.rename("../templates/kanji/gothic extra/"+fmt, "../templates/kanji/gothic/"+fmt)
    #         counter += 1

    # print "moved %d files" % counter

def compare_folders():
    path2 = "../templates/kanji/small gothic dups/"
    path1 = "../templates/kanji//"

    list_path1 = os.listdir(path1)
    list_path2 = os.listdir(path2)

    print "items in %s that are not in %s" % (path1, path2)
    for item in list_path1:
        if item not in list_path2:
            print unichr(int(item.split(".")[0]))

def move_matched_files():
    path1 = "../templates/kanji/small gothic extra/"
    path2 = "../templates/kanji/gothic extra/"
    path3 = "../templates/kanji/small gothic dups/"

    list_path1 = os.listdir(path1)

    for im in list_path1:
        if os.path.exists(path2+im) and not os.path.exists(path3+im):
            os.rename(path1+im, path3+im)
            print im


def delete_duplicates():
    path1 = "../templates/kanji/mincho extra/"
    path2 = "../templates/kanji/mincho/"

    list_path1 = os.listdir(path1)

    bad_items = []
    for item in list_path1:
        if os.path.exists(path2+item):
            bad_items.append(item)
            os.remove(path1+item)

    print bad_items


def find_missing_files():
    list_of_files = os.listdir("../templates/kanji/gothic")
    f = open("missing.txt")
    missing_files = f.readlines()

    print len(missing_files)

    for mf in missing_files:
        if os.path.exists("../templates/kanji/gothic/"+mf):
            os.rename("../templates/kanji/gothic/"+mf, "../templates/kanji/gothic extra/"+mf)

    # counter = 0
    # for c in code_points:
    #     fmt = str(c) + ".bmp"
    #     if fmt in list_of_files and not os.path.exists("../templates/kanji/gothic/"+fmt):
    #         os.rename("../templates/kanji/gothic extra/"+fmt, "../templates/kanji/gothic/"+fmt)
    #         counter += 1

    # print "moved %d files" % counter

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
    # main()
    # codepts_from_chars()
    # compare_folders()
    # create_list_of_unicode_strings_from_list()
    # find_missing_files()
    # delete_duplicates()
    move_matched_files()