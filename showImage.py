import numpy as np
from scipy.misc import imread, imresize
import matplotlib.pyplot as plt

img1 = imread('./local_data/dateofbirth.png')
img2 = imread('./local_data/hovaten.png')


# Show the original image
plt.subplot(1, 2, 1)
plt.imshow(img1)

# Show the tinted image
plt.subplot(1, 2, 2)

# A slight gotcha with imshow is that it might give strange results
# if presented with data that is not uint8. To work around this, we
# explicitly cast the image to uint8 before displaying it.
plt.imshow(img2)
plt.show()