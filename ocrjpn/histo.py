# import numpy as np
import matplotlib.pyplot as plt

f = open("islands.txt")
lines = f.readlines()
f.close()

# blacks = [ int(line.split()[0]) for line in lines ]
# whites = [ int(line.split()[1]) for line in lines ]

# N = 50
# area = np.pi * (15 * np.random.rand(N))**2 # 0 to 15 point radiuses

# plt.scatter(blacks, whites, s=area, alpha=0.5)

# plt.show()

four_six = 0
five_three = 0

pts = [(4, 6), (5, 3), (7, 6), (8, 6), (2, 8), (2, 4), (2, 6), (2,9)]
sums = {}


for line in lines:
    count = sums.get(line, 0)
    count += 1
    sums[line] = count

# big_buckets = 0

# for key, value in sums.items():
#     if value > 80:
#         print key.strip() + ":", value
#         big_buckets += 1

print "Total number of buckets:", len(sums.keys())

print sums["2 4\n"]

print sums["1 4\n"]
print sums["3 4\n"]
print sums["2 5\n"]
print sums["2 3\n"]

# plt.hist( sums.values() )
# plt.show()
# print "Number of buckets over 80:", big_buckets