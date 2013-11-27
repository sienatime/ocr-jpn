import cProfile
import recognize
cProfile.run('recognize.main("../test_images/jouchi.bmp", "kanji")')