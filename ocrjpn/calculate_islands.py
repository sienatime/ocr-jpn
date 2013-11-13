from PIL import Image
from find_islands import find_islands
import os

def main():
    path = "../templates/kanji/mincho/"
    list_of_files = os.listdir(path)

    for img in list_of_files:
        im = Image.open(path+img).convert("L")

        black, white = find_islands(im)
        print black, white

if __name__ == "__main__":
    main()