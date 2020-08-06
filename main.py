import logging as log
import argparse as arg
import cv2 as cv
import math as math
import os as os
import numpy as np
from PIL import Image
from PIL import ImageFilter

import SupportMainFunctions as smf
import SupportMainClasses as smc

'-------------------------------------------------------------------------------------'
'setup logger'
log.basicConfig(level=log.DEBUG, filename='temp/log.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

'-------------------------------------------------------------------------------------'
'setup csv to log detected point data'

try:
    os.remove('temp/pointData.csv')
    csvWriter = open('temp/pointData.csv', 'a', newline='')
except:
    print("Error while deleting file ", 'temp/pointData.csv')

csvWriter = open('temp/pointData.csv', 'a', newline='')

'-------------------------------------------------------------------------------------'
'setup arguments'
parser = arg.ArgumentParser()
parser.add_argument('--inputPath', help="path to input Video", default='resources/MVI_9105.MOV')

args = parser.parse_args()

log.info("Video Path : '{}'".format(args.inputPath))

'-------------------------------------------------------------------------------------'
'Video Capture Init'
capture = cv.VideoCapture(args.inputPath)
capture2 = cv.VideoCapture(args.inputPath)
'Background substraction init'
backSub = cv.createBackgroundSubtractorKNN(history=200, dist2Threshold=500.0, detectShadows=False)

'Get Video Properties'
frame_count = capture.get(cv.CAP_PROP_FRAME_COUNT)
frame_width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
frame_height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
fps = capture.get(cv.CAP_PROP_FPS)
video_codec = capture.get(cv.CAP_PROP_FOURCC)
video_name = args.inputPath.split(".")[0].split("/")[1]

'Log Properties'
log.info("Total Number of Frames : '{}'".format(frame_count))
log.info("Frame width : '{}'".format(frame_width))
log.info("Frame height : '{}'".format(frame_height))
log.info("FPS : '{}'".format(fps))
log.info("Video Codec : '{}'".format(smf.decode_fourcc(video_codec)))
log.info("Video Name : '{}'".format(video_name))

'-------------------------------------------------------------------------------------'
'Video Writer Init'
fourcc = cv.VideoWriter_fourcc(*'avc1')
writer = cv.VideoWriter('temp/output.MOV', fourcc, int(fps), (int(frame_width), int(frame_height)), True)

# User input for each point
flag, frame = capture2.read()
frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

x0, y0, r0, g0, b0 = smc.Pixelcollector(frame).getXYRGB()

x1, y1, r1, g1, b1 = smc.Pixelcollector(frame).getXYRGB()
x2, y2, r2, g2, b2 = smc.Pixelcollector(frame).getXYRGB()
x3, y3, r3, g3, b3 = smc.Pixelcollector(frame).getXYRGB()

x4, y4, r4, g4, b4 = smc.Pixelcollector(frame).getXYRGB()
x5, y5, r5, g5, b5 = smc.Pixelcollector(frame).getXYRGB()
x6, y6, r6, g6, b6 = smc.Pixelcollector(frame).getXYRGB()

# range between picked points
lenghtP01 = round(math.hypot(x1 - x0, y1 - y0))
lenghtP12 = round(math.hypot(x2 - x1, y2 - y1))
lenghtP23 = round(math.hypot(x3 - x2, y3 - y2))

lenghtP34 = round(math.hypot(x4 - x3, y4 - y3))
lenghtP45 = round(math.hypot(x5 - x4, y5 - y4))
lenghtP56 = round(math.hypot(x6 - x5, y6 - y5))

# convert to HSV
picked_p1 = smf.BGR2CVHSV(b1, g1, r1)
picked_p2 = smf.BGR2CVHSV(b2, g2, r2)
picked_p3 = smf.BGR2CVHSV(b3, g3, r3)

picked_p4 = smf.BGR2CVHSV(b4, g4, r4)
picked_p5 = smf.BGR2CVHSV(b5, g5, r5)
picked_p6 = smf.BGR2CVHSV(b6, g6, r6)

# define Color Range in HSV
hColorRange_p1, sColorRange_p1, vColorRange_p1 = 20, 50, 80
hColorRange_p2, sColorRange_p2, vColorRange_p2 = 30, 60, 80
hColorRange_p3, sColorRange_p3, vColorRange_p3 = 20, 50, 80
hColorRange_p4, sColorRange_p4, vColorRange_p4 = 20, 50, 80
hColorRange_p5, sColorRange_p5, vColorRange_p5 = 20, 50, 80
hColorRange_p6, sColorRange_p6, vColorRange_p6 = 30, 60, 80

lower_p1 = (picked_p1[0] - hColorRange_p1 if picked_p1[0] - hColorRange_p1 > 0 else 0,
            picked_p1[1] - sColorRange_p1 if picked_p1[1] - sColorRange_p1 > 0 else 0,
            picked_p1[2] - vColorRange_p1 if picked_p1[2] - vColorRange_p1 > 0 else 0)
upper_p1 = (picked_p1[0] + hColorRange_p1 if picked_p1[0] + hColorRange_p1 < 180 else 180,
            picked_p1[1] + sColorRange_p1 if picked_p1[1] + sColorRange_p1 < 255 else 255,
            picked_p1[2] + vColorRange_p1 if picked_p1[2] + vColorRange_p1 < 255 else 255)

lower_p2 = (picked_p2[0] - hColorRange_p2 if picked_p2[0] - hColorRange_p2 > 0 else 0,
            picked_p2[1] - sColorRange_p2 if picked_p2[1] - sColorRange_p2 > 0 else 0,
            picked_p2[2] - vColorRange_p2 if picked_p2[2] - vColorRange_p2 > 0 else 0)
upper_p2 = (picked_p2[0] + hColorRange_p2 if picked_p2[0] + hColorRange_p2 < 180 else 180,
            picked_p2[1] + sColorRange_p2 if picked_p2[1] + sColorRange_p2 < 255 else 255,
            picked_p2[2] + vColorRange_p2 if picked_p2[2] + vColorRange_p2 < 255 else 255)

lower_p3 = (picked_p3[0] - hColorRange_p3 if picked_p3[0] - hColorRange_p3 > 0 else 0,
            picked_p3[1] - sColorRange_p3 if picked_p3[1] - sColorRange_p3 > 0 else 0,
            picked_p3[2] - vColorRange_p3 if picked_p3[2] - vColorRange_p3 > 0 else 0)
upper_p3 = (picked_p3[0] + hColorRange_p3 if picked_p3[0] + hColorRange_p3 < 180 else 180,
            picked_p3[1] + sColorRange_p3 if picked_p3[1] + sColorRange_p3 < 255 else 255,
            picked_p3[2] + vColorRange_p3 if picked_p3[2] + vColorRange_p3 < 255 else 255)

lower_p4 = (picked_p4[0] - hColorRange_p4 if picked_p4[0] - hColorRange_p4 > 0 else 0,
            picked_p4[1] - sColorRange_p4 if picked_p4[1] - sColorRange_p4 > 0 else 0,
            picked_p4[2] - vColorRange_p4 if picked_p4[2] - vColorRange_p4 > 0 else 0)
upper_p4 = (picked_p4[0] + hColorRange_p4 if picked_p4[0] + hColorRange_p4 < 180 else 180,
            picked_p4[1] + sColorRange_p4 if picked_p4[1] + sColorRange_p4 < 255 else 255,
            picked_p4[2] + vColorRange_p4 if picked_p4[2] + vColorRange_p4 < 255 else 255)

lower_p5 = (picked_p5[0] - hColorRange_p5 if picked_p5[0] - hColorRange_p5 > 0 else 0,
            picked_p5[1] - sColorRange_p5 if picked_p5[1] - sColorRange_p5 > 0 else 0,
            picked_p5[2] - vColorRange_p5 if picked_p5[2] - vColorRange_p5 > 0 else 0)
upper_p5 = (picked_p5[0] + hColorRange_p5 if picked_p5[0] + hColorRange_p5 < 180 else 180,
            picked_p5[1] + sColorRange_p5 if picked_p5[1] + sColorRange_p5 < 255 else 255,
            picked_p5[2] + vColorRange_p5 if picked_p5[2] + vColorRange_p5 < 255 else 255)

lower_p6 = (picked_p6[0] - hColorRange_p6 if picked_p6[0] - hColorRange_p6 > 0 else 0,
            picked_p6[1] - sColorRange_p6 if picked_p6[1] - sColorRange_p6 > 0 else 0,
            picked_p6[2] - vColorRange_p6 if picked_p6[2] - vColorRange_p6 > 0 else 0)
upper_p6 = (picked_p6[0] + hColorRange_p6 if picked_p6[0] + hColorRange_p6 < 180 else 180,
            picked_p6[1] + sColorRange_p6 if picked_p6[1] + sColorRange_p6 < 255 else 255,
            picked_p6[2] + vColorRange_p6 if picked_p6[2] + vColorRange_p6 < 255 else 255)

print(lower_p6)
print(upper_p6)

#Jedes 5te frame eines Videos an den KNN-Background leaner übergeben

for x in range(0, 200):
    flag, frame = capture.read()
    if flag is True and x % 5 == 0:
        # Foreground Mask
        fgMask = backSub.apply(frame)
capture.release()
capture = cv.VideoCapture(args.inputPath)


'Work'
while capture.isOpened():
    flag, frame = capture.read()
    if flag is True:

        frame2 = np.copy(frame)
        # Foreground Mask
        fgMask = backSub.apply(frame)
        fgMaskBlurred = smf.blurandthresh(fgMask, 50, (51, 51))
        #fgMask = smf.blurandthresh(fgMask, 50, (5, 5))

        # Color Masks
        p1Mask = cv.inRange(cv.cvtColor(frame, cv.COLOR_BGR2HSV), lower_p1, upper_p1)
        p2Mask = cv.inRange(cv.cvtColor(frame, cv.COLOR_BGR2HSV), lower_p2, upper_p2)
        p3Mask = cv.inRange(cv.cvtColor(frame, cv.COLOR_BGR2HSV), lower_p3, upper_p3)
        p4Mask = cv.inRange(cv.cvtColor(frame, cv.COLOR_BGR2HSV), lower_p4, upper_p4)
        p5Mask = cv.inRange(cv.cvtColor(frame, cv.COLOR_BGR2HSV), lower_p5, upper_p5)
        p6Mask = cv.inRange(cv.cvtColor(frame, cv.COLOR_BGR2HSV), lower_p6, upper_p6)

        p1Mask = smf.blurandthresh(p1Mask, 50, (51, 51))
        p2Mask = smf.blurandthresh(p2Mask, 50, (51, 51))
        p3Mask = smf.blurandthresh(p3Mask, 50, (51, 51))
        p4Mask = smf.blurandthresh(p4Mask, 50, (51, 51))
        p5Mask = smf.blurandthresh(p5Mask, 50, (51, 51))
        p6Mask = smf.blurandthresh(p6Mask, 50, (51, 51))

        # Final Mask
        p1CombinedMaske = cv.bitwise_and(p1Mask, fgMaskBlurred, mask=None)
        p2CombinedMaske = cv.bitwise_and(p2Mask, fgMaskBlurred, mask=None)
        p3CombinedMaske = cv.bitwise_and(p3Mask, fgMaskBlurred, mask=None)
        p4CombinedMaske = cv.bitwise_and(p4Mask, fgMaskBlurred, mask=None)
        p5CombinedMaske = cv.bitwise_and(p5Mask, fgMaskBlurred, mask=None)
        p6CombinedMaske = cv.bitwise_and(p6Mask, fgMaskBlurred, mask=None)

        # Final Mask
        p1CombinedMaske = smf.blurandthresh(p1CombinedMaske, 50, (15, 15))
        p2CombinedMaske = smf.blurandthresh(p2CombinedMaske, 50, (15, 15))
        p3CombinedMaske = smf.blurandthresh(p3CombinedMaske, 50, (15, 15))
        p4CombinedMaske = smf.blurandthresh(p4CombinedMaske, 50, (15, 15))
        p5CombinedMaske = smf.blurandthresh(p5CombinedMaske, 50, (15, 15))
        p6CombinedMaske = smf.blurandthresh(p6CombinedMaske, 50, (15, 15))

        high_thresh1, thresh_im = cv.threshold(p1CombinedMaske, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        lowThresh1 = 0.5 * high_thresh1
        high_thresh2, thresh_im = cv.threshold(p2CombinedMaske, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        lowThresh2 = 0.5 * high_thresh2
        high_thresh3, thresh_im = cv.threshold(p3CombinedMaske, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        lowThresh3 = 0.5 * high_thresh3
        high_thresh4, thresh_im = cv.threshold(p4CombinedMaske, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        lowThresh4 = 0.5 * high_thresh4
        high_thresh5, thresh_im = cv.threshold(p5CombinedMaske, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        lowThresh5 = 0.5 * high_thresh5
        high_thresh6, thresh_im = cv.threshold(p6CombinedMaske, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        lowThresh6 = 0.5 * high_thresh6

        p1Canny = cv.Canny(p1CombinedMaske,high_thresh1,lowThresh1)
        p2Canny = cv.Canny(p2CombinedMaske,high_thresh2,lowThresh2)
        p3Canny = cv.Canny(p3CombinedMaske,high_thresh3,lowThresh3)
        p4Canny = cv.Canny(p4CombinedMaske,high_thresh4,lowThresh4)
        p5Canny = cv.Canny(p5CombinedMaske,high_thresh5,lowThresh5)
        p6Canny = cv.Canny(p6CombinedMaske,high_thresh6,lowThresh6)


        # Apply HoughCircle transform on the blurred image.
        detected_circles_p1 = cv.HoughCircles(p1Canny, cv.HOUGH_GRADIENT, 1, 20, param1=5, param2=10, minRadius=1, maxRadius=30)
        detected_circles_p2 = cv.HoughCircles(p2Canny, cv.HOUGH_GRADIENT, 1, 20, param1=5, param2=10, minRadius=1, maxRadius=30)
        detected_circles_p3 = cv.HoughCircles(p3Canny, cv.HOUGH_GRADIENT, 1, 20, param1=5, param2=10, minRadius=1, maxRadius=30)
        detected_circles_p4 = cv.HoughCircles(p4Canny, cv.HOUGH_GRADIENT, 1, 20, param1=5, param2=10, minRadius=1, maxRadius=30)
        detected_circles_p5 = cv.HoughCircles(p5Canny, cv.HOUGH_GRADIENT, 1, 20, param1=5, param2=10, minRadius=1, maxRadius=30)
        detected_circles_p6 = cv.HoughCircles(p6Canny, cv.HOUGH_GRADIENT, 1, 20, param1=5, param2=10, minRadius=1, maxRadius=30)

        # calculate Point positions
        if detected_circles_p1 is not None and detected_circles_p2 is not None and detected_circles_p3 is not None and detected_circles_p4 is not None and detected_circles_p5 is not None and detected_circles_p6 is not None:

            # Calculate P1 by range of users inputrange and P0
            calclenghtP01 = []
            for pointP1 in detected_circles_p1[0]:
                calclenghtP01.append(round(math.hypot(pointP1[0] - x0, pointP1[1] - y0)))
            calcP1 = detected_circles_p1[0][smf.find_nearest(calclenghtP01, lenghtP01)]

            # Calculate P2 by range of users inputrange and P1
            calclenghtP12 = []
            for pointP2 in detected_circles_p2[0]:
                calclenghtP12.append(round(math.hypot(pointP2[0] - calcP1[0], pointP2[1] - calcP1[1])))
            calcP2 = detected_circles_p2[0][smf.find_nearest(calclenghtP12, lenghtP12)]

            # Calculate P3 by range of users Inputrange and P2
            calclenghtP23 = []
            for pointP3 in detected_circles_p3[0]:
                calclenghtP23.append(round(math.hypot(pointP3[0] - calcP2[0], pointP3[1] - calcP2[1])))
            calcP3 = detected_circles_p3[0][smf.find_nearest(calclenghtP23, lenghtP23)]

            # Calculate P4 by range of users Inputrange and P3
            calclenghtP34 = []
            for pointP4 in detected_circles_p4[0]:
                calclenghtP34.append(round(math.hypot(pointP4[0] - calcP3[0], pointP4[1] - calcP3[1])))
            calcP4 = detected_circles_p4[0][smf.find_nearest(calclenghtP34, lenghtP34)]

            # Calculate P5 by range of users Inputrange and P4
            calclenghtP45 = []
            for pointP5 in detected_circles_p5[0]:
                calclenghtP45.append(round(math.hypot(pointP5[0] - calcP4[0], pointP5[1] - calcP4[1])))
            calcP5 = detected_circles_p5[0][smf.find_nearest(calclenghtP45, lenghtP45)]

            # Calculate P6 by range of users Inputrange and P5
            calclenghtP56 = []
            for pointP6 in detected_circles_p6[0]:
                calclenghtP56.append(round(math.hypot(pointP6[0] - calcP5[0], pointP6[1] - calcP5[1])))
            calcP6 = detected_circles_p6[0][smf.find_nearest(calclenghtP56, lenghtP56)]

        else:

            if detected_circles_p1 is None:
                log.info("Missing Circle P1 in frame Nr : '{}'".format(capture.get(cv.CAP_PROP_POS_FRAMES)))
            if detected_circles_p2 is None:
                log.info("Missing Circle P2 in frame Nr : '{}'".format(capture.get(cv.CAP_PROP_POS_FRAMES)))
            if detected_circles_p3 is None:
                log.info("Missing Circle P3 in frame Nr : '{}'".format(capture.get(cv.CAP_PROP_POS_FRAMES)))
            if detected_circles_p4 is None:
                log.info("Missing Circle P4 in frame Nr : '{}'".format(capture.get(cv.CAP_PROP_POS_FRAMES)))
            if detected_circles_p5 is None:
                log.info("Missing Circle P5 in frame Nr : '{}'".format(capture.get(cv.CAP_PROP_POS_FRAMES)))
            if detected_circles_p6 is None:
                log.info("Missing Circle P6 in frame Nr : '{}'".format(capture.get(cv.CAP_PROP_POS_FRAMES)))


            x1, y1 = smc.Pixelcollector(frame).getXY()
            x2, y2 = smc.Pixelcollector(frame).getXY()
            x3, y3 = smc.Pixelcollector(frame).getXY()
            x4, y4 = smc.Pixelcollector(frame).getXY()
            x5, y5 = smc.Pixelcollector(frame).getXY()
            x6, y6 = smc.Pixelcollector(frame).getXY()

            calcP1[0] = x1
            calcP1[1] = y1
            calcP1[2] = 1
            calcP2[0] = x2
            calcP2[1] = y2
            calcP2[2] = 1
            calcP3[0] = x3
            calcP3[1] = y3
            calcP3[2] = 1
            calcP4[0] = x4
            calcP4[1] = y4
            calcP4[2] = 1
            calcP5[0] = x5
            calcP5[1] = y5
            calcP5[2] = 1
            calcP6[0] = x6
            calcP6[1] = y6
            calcP6[2] = 1

        # Draw the circumference of the circle.
        cv.line(frame, (x0 + 20, y0), (x0 - 20, y0), (0, 0, 0), 5)
        cv.line(frame, (x0, y0 + 20), (x0 , y0 - 20), (0, 0, 0), 5)

        cv.line(frame, (int(calcP1[0]) + 20, int(calcP1[1])), (int(calcP1[0]) - 20, int(calcP1[1])), (0, 255, 255), 5)
        cv.line(frame, (int(calcP1[0]), int(calcP1[1]) + 20), (int(calcP1[0]), int(calcP1[1]) - 20), (0, 255, 255), 5)

        cv.line(frame, (int(calcP2[0]) + 20, int(calcP2[1])), (int(calcP2[0]) - 20, int(calcP2[1])), (0, 0, 255), 5)
        cv.line(frame, (int(calcP2[0]), int(calcP2[1]) + 20), (int(calcP2[0]), int(calcP2[1]) - 20), (0, 0, 255), 5)

        cv.line(frame, (int(calcP3[0]) + 20, int(calcP3[1])), (int(calcP3[0]) - 20, int(calcP3[1])), (70, 0, 130), 5)
        cv.line(frame, (int(calcP3[0]), int(calcP3[1]) + 20), (int(calcP3[0]), int(calcP3[1]) - 20), (70, 0, 130), 5)

        cv.line(frame, (int(calcP4[0]) + 20, int(calcP4[1])), (int(calcP4[0]) - 20, int(calcP4[1])), (255, 0, 0), 5)
        cv.line(frame, (int(calcP4[0]), int(calcP4[1]) + 20), (int(calcP4[0]), int(calcP4[1]) - 20), (255, 0, 0), 5)

        cv.line(frame, (int(calcP5[0]) + 20, int(calcP5[1])), (int(calcP5[0]) - 20, int(calcP5[1])), (0, 80, 255), 5)
        cv.line(frame, (int(calcP5[0]), int(calcP5[1]) + 20), (int(calcP5[0]), int(calcP5[1]) - 20), (0, 80, 255), 5)

        cv.line(frame, (int(calcP6[0]) + 20, int(calcP6[1])), (int(calcP6[0]) - 20, int(calcP6[1])), (0, 255, 55), 5)
        cv.line(frame, (int(calcP6[0]), int(calcP6[1]) + 20), (int(calcP6[0]), int(calcP6[1]) - 20), (0, 255, 55), 5)

        # Write Point Data to csv
        csvWriter.write(str(x0) + ", " + str(y0) + ", " +
                        str(calcP1[0]) + ", " + str(calcP1[1]) + ", " +
                        str(calcP2[0]) + ", " + str(calcP2[1]) + ", " +
                        str(calcP3[0]) + ", " + str(calcP3[1]) + ", " +
                        str(calcP4[0]) + ", " + str(calcP4[1]) + ", " +
                        str(calcP5[0]) + ", " + str(calcP5[1]) + ", " +
                        str(calcP6[0]) + ", " + str(calcP6[1]) + "\n" )

        # show current frame with frame nr
        cv.rectangle(frame, (0, 0), (100, 25), (255, 255, 255), -1)
        cv.putText(frame, "Frame: " + str(capture.get(cv.CAP_PROP_POS_FRAMES)), (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                   (0, 0, 0))

        cv.rectangle(frame, (0, 25), (100, 50), (b1, g1, r1), -1)
        cv.rectangle(frame, (0, 50), (100, 75), (b2, g2, r2), -1)
        cv.rectangle(frame, (0, 75), (100, 100), (b3, g3, r3), -1)
        cv.rectangle(frame, (0, 100), (100, 125), (b4, g4, r4), -1)
        cv.rectangle(frame, (0, 125), (100, 150), (b5, g5, r5), -1)
        cv.rectangle(frame, (0, 150), (100, 175), (b6, g6, r6), -1)

        # define window size
        cv.namedWindow('p0', cv.WINDOW_NORMAL)
        cv.resizeWindow('p0', 1440, 810)
        # define window size
        cv.namedWindow('p1', cv.WINDOW_NORMAL)
        cv.resizeWindow('p1', 1440, 810)
        # define window size
        cv.namedWindow('p2', cv.WINDOW_NORMAL)
        cv.resizeWindow('p2', 1440, 810)
        # define window size
        cv.namedWindow('p3', cv.WINDOW_NORMAL)
        cv.resizeWindow('p3', 1440, 810)
        # define window size
        cv.namedWindow('p4', cv.WINDOW_NORMAL)
        cv.resizeWindow('p4', 1440, 810)
        # define window size
        cv.namedWindow('p5', cv.WINDOW_NORMAL)
        cv.resizeWindow('p5', 1440, 810)
        # define window size
        cv.namedWindow('p6', cv.WINDOW_NORMAL)
        cv.resizeWindow('p6', 1440, 810)
        # define window size
        cv.namedWindow('p8', cv.WINDOW_NORMAL)
        cv.resizeWindow('p8', 1440, 810)

        p7Maske = cv.bitwise_or(p1CombinedMaske, cv.bitwise_or(p2CombinedMaske, cv.bitwise_or(p3CombinedMaske, cv.bitwise_or(p4CombinedMaske,cv.bitwise_or(p5CombinedMaske, p6CombinedMaske)))))

        cv.imshow('p0', frame)
        cv.imshow('p1', fgMask)
        cv.imshow('p2', fgMaskBlurred)
        cv.imshow('p3', p4Mask)
        cv.imshow('p4', frame2)
        cv.imshow('p8', p4Canny)
        cv.imshow('p5', p7Maske)
        asdf = cv.bitwise_and(frame2, frame2, mask=p7Maske)
        cv.imshow('p6', p4CombinedMaske)
        # quit hook
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        # write Frame to video
        writer.write(frame)


    else:
        break

'Releasrelease everything'
capture.release()
writer.release()
csvWriter.close()
cv.destroyAllWindows()
