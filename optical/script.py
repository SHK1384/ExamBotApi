from functools import cmp_to_key

import cv2
import numpy as np
from . import utils


def process_image(img_byte):
    ################
    widthImg = 500
    heightImg = int(widthImg*1.4142)
    ################

    np_ar = np.frombuffer(img_byte, np.uint8)
    img = cv2.imdecode(np_ar, cv2.IMREAD_COLOR)

    img = cv2.resize(img, (widthImg, heightImg))
    imgContours = img.copy()
    imgBiggestContours = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 150, 300)

    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 1)

    # cv2.imshow("hi", imgCanny)
    # cv2.waitKey(0)

    rectCon = utils.rectContours(contours)
    cv2.drawContours(imgContours, rectCon, -1, (0, 255, 0), 1)
    # cv2.imshow("hi", imgContours)
    # cv2.waitKey(0)
    if len(rectCon) <= 7:
        return "Bad"

    answers = rectCon[2:8]
    # cv2.drawContours(imgContours, answers, -1, (0, 255, 0), 1)
    # cv2.imshow("hi", imgContours)
    # cv2.waitKey(0)


    if cv2.contourArea(answers[0]) - cv2.contourArea(answers[-1]) >= 1500:
        return "Bad"

    answers_corner_points = []

    for answer in answers:
        corner = utils.getCornerPoins(answer)
        corner = utils.reorder(corner)
        answers_corner_points.append(corner)
        cv2.drawContours(imgBiggestContours, [corner[0]] , -1, (0, 255, 0), 10)


    imgCorner = img.copy()

    def cmp(a, b):
        if abs(a[0][0][0] - b[0][0][0]) < 50:
            if a[0][0][1] < b[0][0][1]:
                return -1
            elif a[0][0][1] > b[0][0][1]:
                return 1
            else:
                return 0
        elif a[0][0][0] < b[0][0][0]:
            return -1
        elif a[0][0][0] > b[0][0][0]:
            return 1

    answers_corner_points = sorted(answers_corner_points, key=cmp_to_key(cmp))

    cv2.drawContours(imgCorner, answers_corner_points[0], -1, (0, 255, 0), 10) #green
    cv2.drawContours(imgCorner, answers_corner_points[1], -1, (255, 0, 0), 10) #blue
    cv2.drawContours(imgCorner, answers_corner_points[2], -1, (0, 0, 255), 10) #red
    cv2.drawContours(imgCorner, answers_corner_points[3], -1, (0, 255, 255), 10) #yellow
    cv2.drawContours(imgCorner, answers_corner_points[4], -1, (255, 255, 0), 10) #cyan
    cv2.drawContours(imgCorner, answers_corner_points[5], -1, (255, 0, 255), 10) #magenta

    ans = []
    for i in utils.grided(answers_corner_points[0], widthImg, heightImg, img):
        ans.append(i)
    for i in utils.grided(answers_corner_points[1], widthImg, heightImg, img):
        ans.append(i)
    for i in utils.grided(answers_corner_points[2], widthImg, heightImg, img):
        ans.append(i)
    for i in utils.grided(answers_corner_points[3], widthImg, heightImg, img):
        ans.append(i)
    for i in utils.grided(answers_corner_points[4], widthImg, heightImg, img):
        ans.append(i)
    for i in utils.grided(answers_corner_points[5], widthImg, heightImg, img):
        ans.append(i)

    # cv2.imshow("hi", imgCorner)
    #cv2.imshow("hi", imgGridWarpedGray)

    # cv2.waitKey(0)
    return ans
