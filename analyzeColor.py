from PIL import Image


csvFile = open("./local_data/histogram.csv", 'w')
img = Image.open("./local_data/dateofbirth.png")
(w, h) = img.size
pixdata1 = img.load()

num_bin = 128
bin_size = 256 / num_bin

r = [0 for _ in range(num_bin)]
g = [0 for _ in range(num_bin)]
b = [0 for _ in range(num_bin)]
for i in range(w):
    for j in range(h):
        if sum(pixdata1[i, j]) > 100 * 3:
            continue
        r[int(1.0 * pixdata1[i, j][0] / bin_size)] += 1
        g[int(1.0 * pixdata1[i, j][1] / bin_size)] += 1
        b[int(1.0 * pixdata1[i, j][2] / bin_size)] += 1
for val in r:
    csvFile.write(str(val) + ',')
csvFile.write('\n')
for val in g:
    csvFile.write(str(val) + ',')
csvFile.write('\n')
for val in b:
    csvFile.write(str(val) + ',')
csvFile.write('\n')

img = Image.open("./local_data/hovaten.png")
(w, h) = img.size
pixdata1 = img.load()
r = [0 for _ in range(num_bin)]
g = [0 for _ in range(num_bin)]
b = [0 for _ in range(num_bin)]
for i in range(w):
    for j in range(h):
        if sum(pixdata1[i, j]) > 100 * 3:
            continue
        r[int(1.0 * pixdata1[i, j][0] / bin_size)] += 1
        g[int(1.0 * pixdata1[i, j][1] / bin_size)] += 1
        b[int(1.0 * pixdata1[i, j][2] / bin_size)] += 1
for val in r:
    csvFile.write(str(val) + ',')
csvFile.write('\n')
for val in g:
    csvFile.write(str(val) + ',')
csvFile.write('\n')
for val in b:
    csvFile.write(str(val) + ',')
csvFile.write('\n')