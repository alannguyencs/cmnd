from PIL import Image


img = Image.open("./data/1.jpg")

(w, h) = img.size


H = 400
W = int(1.0 * H * w / h)
img = img.resize((W,H), Image.ANTIALIAS)

img.save("./local_data/1.png")



