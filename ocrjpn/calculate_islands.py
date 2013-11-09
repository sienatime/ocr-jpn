from PIL import Image
from recognize import find_islands
import os

def main():
    list_of_files = os.listdir("../templates/test/")

    for img in list_of_files:
        im = Image.open("../templates/test/"+img).convert("L")

        print find_islands(im)

main()