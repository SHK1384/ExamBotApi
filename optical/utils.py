import cv2
import numpy as np

# def stackImages(imgArray, scale, lables=[]):
#     rows = len(imgArray)
#     cols = len(imgArray[0])
#     rowsAvailable = isinstance(imgArray[0], list)
#     width = imgArray[0][0].shape[1]
#     height = imgArray[0][0].shape[0]
#     if rowsAvailable:
#         for x in range(0, rows):
#             for y in range(0, cols):
#                 imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
#                 if len(imgArray[x][y].shape) == 2:
#                     imgArray[x][y] = imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
#         imageBlank = np.zeros((height, width, 3), np.uint8)
#         hor = np.hstack(imgArray)
#         hor_con = np.concatenate(imgArray)
#         ver = hor
#         if len(lables) != 0:
#             eachImgWidth = int(ver.shape[1]/cols)
#             eachImgHeight = int(ver.shape[0]/rows)
#             for d in range(0, rows):
#                 for c in range(0, cols):
#                     cv2.rectangle(ver, (c*eachImgWidth,eachImgHeight*d), (c*eachImgWidth+len(lables[d][c])*13+27, 30+each)


def rectContours(contours):
    rectCon = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > 17000:
            prei = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * prei, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea, reverse=True)

    return rectCon

def getCornerPoins(cont):
    prei = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.02 * prei, True)
    return approx

def reorder(mpoints):
    mpoints = mpoints.reshape((4, 2))
    pointsNew = np.zeros((4, 1, 2), np.int32)
    add = mpoints.sum(1)
    pointsNew[3] = mpoints[np.argmax(add)]
    pointsNew[0] = mpoints[np.argmin(add)]
    diff = np.diff(mpoints, axis=1)
    pointsNew[1] = mpoints[np.argmin(diff)]
    pointsNew[2] = mpoints[np.argmax(diff)]

    return pointsNew

def splitBoxes(img):
    rows = np.array_split(img, 10, axis=0)
    boxes = []
    for r in rows:
        cols = np.array_split(r, 5, axis=1)
        rs = []
        for box in cols:
            rs.append(box)
        boxes.append(rs)
    return boxes


def draw_grid(image, n, m, color=(0, 255, 0), thickness=2):
    """
    Draw an N x M grid on the image.

    :param image: Input image
    :param n: Number of rows
    :param m: Number of columns
    :param color: Color of grid lines (default: green)
    :param thickness: Thickness of grid lines (default: 2)
    :return: Image with grid
    """
    height, width = image.shape
    row_height = height // n  # Height of each row
    col_width = width // m  # Width of each column

    # Draw horizontal lines
    for i in range(1, n):
        y = i * row_height
        cv2.line(image, (0, y), (width, y), color, thickness)

    # Draw vertical lines
    for j in range(1, m):
        x = j * col_width
        cv2.line(image, (x, 0), (x, height), color, thickness)

    return image

def grided(corners, widthImg, heightImg, img):
    pt1 = np.float32(corners)
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpGray, 190, 255, cv2.THRESH_BINARY_INV)[1]

    imgThresh = imgThresh[:, 90:]
    imgThresh = imgThresh[10:len(imgThresh)-10, 10:len(imgThresh[0])-10]

    splitBoxes(imgThresh)

    boxes = splitBoxes(imgThresh)

    grid = []

    for row in boxes:
        t = []
        for cols in row:
            if cv2.countNonZero(cols) > 2500:
                t.append(1)
                # print(1, end='')
            else:
                t.append(0)
                # print(0, end='')
        # print()
        grid.append(t)

    return grid
