from PIL import Image

target = '1'

img = Image.open("./data/" + target + ".jpg")
(w, h) = img.size


H = 400
W = int(1.0 * H * w / h)
img = img.resize((W,H), Image.ANTIALIAS)
pixdata = img.load()

red = Image.new('L', (W, H))
reddata = red.load()
print (W, H)
for i in range(W):
    for j in range(H):
        reddata[i, j] = max(0, 2 * pixdata[i, j][2] - pixdata[i, j][0] - pixdata[i, j][1])
        if reddata[i, j] < 64:
            reddata[i, j] = 255
        else:
            reddata[i, j] = 0

red.save("./blue_images/" + target + ".png")
