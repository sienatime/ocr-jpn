from PIL import Image
from islands import find_islands
import os
import memcache


class KanjiObj(object):
    def __init__(self, vals, black, white, code=None):
        self.id = code
        self.vals = vals
        self.blacks = black
        self.whites = white

def main():
    mc = memcache.Client(['127.0.0.1:11211'], debug=1)
    path = "../templates/hiragana/gothic/"
    list_of_files = os.listdir(path)

    for img in list_of_files:
        im = Image.open(path+img).convert("L")

        black, white = find_islands(im)

        code = img.split(".")[0]

        new_obj = KanjiObj(list(im.getdata()), black, white, code)

        mc.set(code, new_obj)



if __name__ == "__main__":
    main()