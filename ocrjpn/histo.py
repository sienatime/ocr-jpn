import numpy as np
import matplotlib.pyplot as plt

f = open("kanji_mincho.txt")
lines = f.readlines()
f.close()

blacks = [ int(line.split()[0]) for line in lines ]
# whites = [ int(line.split()[1]) for line in lines ]

plt.hist(blacks, bins = range(15))

plt.show()

# plt.hist(whites, bins = range(15))

# plt.show()