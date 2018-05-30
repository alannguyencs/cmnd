#work with binaryImages_v5
#resize singleImages of single components
#drawBoundingbox
#generate bounding box file
#generate label file
#the same with v4, but add label to bounding box

from PIL import Image
import queue
import glob
import os
from shutil import copyfile
import math



dataPath = "D:/PycharmProjects/cmnd/red_images/"
resultPath = "D:/PycharmProjects/cmnd/components/"
if not os.path.exists(resultPath):
    os.mkdir(resultPath)



def isInsideBox(x, y, width, height):
    if x < 0 or x >= width:
        return False
    if y < 0 or y >= height:
        return False
    return True

def collectConnectedComponents(imgName): #imgID start from 0
    img = Image.open(dataPath + '/' + imgName).convert('L')
    cntList = []
    subResultPath = resultPath + '/' + imgName.split('.')[0]
    if not os.path.exists(subResultPath):
        os.mkdir(subResultPath)

    pixdata = img.load()
    (width, height) = img.size
    q = queue.Queue()
    b = [[-1 for i in range(height)] for j in range(width)]
    connectedComponentID = 0
    isGoodConnectedComponent = {}
    isGoodConnectedComponent[-1] = False
    NoConnectedPoints = []
    leftPole = []
    rightPole = []
    upPole = []
    downPole = []
    for i in range(width):
            for j in range(height):
                if pixdata[i, j] < 128 and b[i][j] == -1:
                    b[i][j] = connectedComponentID
                    q.put((i, j))
                    cnt = 0
                    leftPoint = width
                    rightPoint = 0
                    upPoint = height
                    downPoint = 0
                    while not q.empty():
                        cnt += 1
                        p = q.get()
                        leftPoint = min(leftPoint, p[0])
                        rightPoint = max(rightPoint, p[0])
                        upPoint = min(upPoint, p[1])
                        downPoint = max(downPoint, p[1])
                        for id1 in range (-1, 2): #connect weak component like y character
                            for id2 in range (-1, 2):
                                if isInsideBox(p[0] + id1, p[1] + id2, width, height) \
                                        and pixdata[p[0] + id1, p[1] + id2] < 25 and b[p[0] + id1][p[1] + id2] == -1:
                                    b[p[0] + id1][p[1] + id2] = connectedComponentID
                                    q.put((p[0] + id1, p[1] + id2))

                    # print ("cnt = " + str(cnt))
                    NoConnectedPoints.append(cnt)

                    cntList.append(cnt)
                    if cnt > 60 and cnt < 200:
                        isGoodConnectedComponent[connectedComponentID] = True
                        leftPole.append(leftPoint)
                        rightPole.append(rightPoint)
                        upPole.append(upPoint)
                        downPole.append(downPoint)
                        connectedComponentID += 1

                    else:
                        isGoodConnectedComponent[connectedComponentID] = False

    cntList.sort()
    print (cntList)


    # print (leftPole)
    # print (rightPole)
    # print (upPole)
    # print (downPole)

    for i in range(width):
        for j in range(height):
            # print (b[i][j])
            if not isGoodConnectedComponent[b[i][j]]:
                pixdata[i, j] = 255

    #generateLabel file
    # labelFile = open('./results/components_v7/' + writer + '/' + imgName[:-4] + '/label.csv', 'w')
    #bounding box image
    boundingBoxImage = Image.open(dataPath + '/' + imgName).convert('RGB')
    boundingBoxImage_pixdata = boundingBoxImage.load()
    for id in range(len(leftPole)):
        for i in range(leftPole[id], rightPole[id] + 1):
            boundingBoxImage_pixdata[i, upPole[id]] = (255, 0, 0)
            boundingBoxImage_pixdata[i, downPole[id]] = (255, 0, 0)
        for j in range(upPole[id], downPole[id]):
            boundingBoxImage_pixdata[leftPole[id], j] = (255, 0, 0)
            boundingBoxImage_pixdata[rightPole[id], j] = (255, 0, 0)
    boundingBoxImage.save((subResultPath + '/boundingbox.jpg'))

    for id in range(len(leftPole)):
        # step 1: get the max size of the rectangle containing symbol = singleSize
        singleSize = max(rightPole[id] - leftPole[id] + 1, downPole[id] - upPole[id] + 1)

        # step 2: create a new 2D array with the size of (singleSize, singleSize)
        singleImage = Image.new('L', (singleSize, singleSize), "white")
        pixdataSingleImage = singleImage.load()

        # step 3: push values of symbols to new array
        initX = int((singleSize - (rightPole[id] - leftPole[id])) / 2)
        initY = int((singleSize - (downPole[id] - upPole[id])) / 2)

        for i in range(leftPole[id], rightPole[id] + 1):
            for j in range(upPole[id], downPole[id] + 1):

                if b[i][j] == id:
                    pixdataSingleImage[initX + i - leftPole[id], initY + j - upPole[id]] = pixdata[i, j]
                else:
                    pixdataSingleImage[initX + i - leftPole[id], initY + j - upPole[id]] = 255

        # step 4: resize the (singleSize, singleSize) to (SINGLE_SIZE, SINGLE_SIZE)
        FULLSIZE, MARGIN, SIZE = 50, 4, 42
        singleFull = Image.new('L', (FULLSIZE, FULLSIZE), "white")
        pixdataSingleFull = singleFull.load()

        def getValue(i0, j0):
            if i0 < 0 or i0 >= singleSize or j0 < 0 or j0 >= singleSize:
                return 0
            return pixdataSingleImage[i0, j0]

        # gaussian interpolation
        for i in range(SIZE):
            for j in range(SIZE):
                i0 = math.floor(singleSize * i / SIZE)
                j0 = math.floor(singleSize * j / SIZE)
                pixValue = 0.0
                pixValue += 1.0 / 4 * getValue(i0, j0)
                pixValue += 1.0 / 8 * getValue(i0 - 1, j0)
                pixValue += 1.0 / 8 * getValue(i0 + 1, j0)
                pixValue += 1.0 / 8 * getValue(i0, j0 - 1)
                pixValue += 1.0 / 8 * getValue(i0, j0 + 1)
                pixValue += 1.0 / 16 * getValue(i0 + 1, j0 + 1)
                pixValue += 1.0 / 16 * getValue(i0 - 1, j0 + 1)
                pixValue += 1.0 / 16 * getValue(i0 + 1, j0 - 1)
                pixValue += 1.0 / 16 * getValue(i0 - 1, j0 - 1)

                pixdataSingleFull[MARGIN + i, MARGIN + j] = int(round(pixValue / 255.0)) * 255
                # print(i, j, i0, j0, int(round(pixValue / 255.0)) * 255)

        singleFull.save(subResultPath + '/' + str(id+1) + '.jpg')

data = glob.glob(dataPath + '/*.png')

for file in data:

    print (file)
    number = file.split('\\')[-1].split('.')[0]

    imgName = file.split('\\')[-1]
    print (imgName)

    # if imgName != "41.JPG" and imgName != "102.JPG" and imgName != "23.jpg":
    #     continue


    # if int(imgName.split('.')[0]) > 8:
    #     continue

    # create directory to store image
    collectConnectedComponents(imgName)

