import argparse as arg
import cv2 as cv
import pandas as pd
import SupportMainClasses as smc
import numpy as np
import math

'-------------------------------------------------------------------------------------'
'setup arguments'
parser = arg.ArgumentParser()
parser.add_argument('--inputPath', help="path to input Video", default='resources/MVI_9165.MOV')

args = parser.parse_args()

'Video Capture Init'
capture = cv.VideoCapture(args.inputPath)

'Get Video Properties'
frame_count = capture.get(cv.CAP_PROP_FRAME_COUNT)
video_name = args.inputPath.split(".")[0].split("/")[1]

i=0;

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - math.hypot(value[0], value[1]))).argmin()
    return idx

'Work'
while capture.isOpened():
    data = pd.read_csv('resources/MVI_9165e2.csvk', header=None)
    capture.set(1, i)
    flag, frame = capture.read()
    if flag is True:

        # show current frame with frame nr
        cv.rectangle(frame, (0, 0), (100, 25), (255, 255, 255), -1)
        cv.putText(frame, "Frame: " + str(capture.get(cv.CAP_PROP_POS_FRAMES)), (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        cv.line(frame, (int(data[0][i])+20, int(data[1][i])), (int(data[0][i])-20, int(data[1][i])), (0, 0, 0), 5)
        cv.line(frame, (int(data[0][i]), int(data[1][i])+ 20), (int(data[0][i]), int(data[1][i])- 20), (0, 0, 0), 5)

        cv.line(frame, (int(data[2][i])+20, int(data[3][i])), (int(data[2][i])-20, int(data[3][i])), (0, 255, 255), 5)
        cv.line(frame, (int(data[2][i]), int(data[3][i])+ 20), (int(data[2][i]), int(data[3][i])- 20), (0, 255, 255), 5)

        cv.line(frame, (int(data[4][i])+20, int(data[5][i])), (int(data[4][i])-20, int(data[5][i])), (0, 0, 255), 5)
        cv.line(frame, (int(data[4][i]), int(data[5][i])+ 20), (int(data[4][i]), int(data[5][i])- 20), (0, 0, 255), 5)

        cv.line(frame, (int(data[6][i])+20, int(data[7][i])), (int(data[6][i])-20, int(data[7][i])), (70, 0, 130), 5)
        cv.line(frame, (int(data[6][i]), int(data[7][i])+ 20), (int(data[6][i]), int(data[7][i])- 20), (70, 0, 130), 5)

        cv.line(frame, (int(data[8][i])+20, int(data[9][i])), (int(data[8][i])-20, int(data[9][i])), (255, 0, 0), 5)
        cv.line(frame, (int(data[8][i]), int(data[9][i])+ 20), (int(data[8][i]), int(data[9][i])- 20), (255, 0, 0), 5)

        cv.line(frame, (int(data[10][i])+20, int(data[11][i])), (int(data[10][i])-20, int(data[11][i])), (0, 80, 255), 5)
        cv.line(frame, (int(data[10][i]), int(data[11][i])+ 20), (int(data[10][i]), int(data[11][i])- 20), (0, 80, 255), 5)

        cv.line(frame, (int(data[12][i])+20, int(data[13][i])), (int(data[12][i])-20, int(data[13][i])), (0, 255, 55), 5)
        cv.line(frame, (int(data[12][i]), int(data[13][i])+ 20), (int(data[12][i]), int(data[13][i])- 20), (0, 255, 55), 5)


        cv.namedWindow('frame', cv.WINDOW_NORMAL)
        cv.resizeWindow('frame', 1900, 1000)
        cv.imshow('frame', frame)


        key = cv.waitKey(0)
        while key not in [ord('q'),ord('r'), ord('k'), ord('l')]:
            key = cv.waitKey(0)
        if key == ord('r'):

            arr = [math.hypot(int(data[0][i]), int(data[1][i])),
                   math.hypot(int(data[2][i]), int(data[3][i])),
                   math.hypot(int(data[4][i]), int(data[5][i])),
                   math.hypot(int(data[6][i]), int(data[7][i])),
                   math.hypot(int(data[8][i]), int(data[9][i])),
                   math.hypot(int(data[10][i]), int(data[11][i])),
                   math.hypot(int(data[12][i]), int(data[13][i]))]

            markerPoint = smc.Pixelcollector(frame).getXY()
            markerTarget = smc.Pixelcollector(frame).getXY()

            data[find_nearest(arr, markerPoint) *2][i] = markerTarget[0]
            data[(find_nearest(arr, markerPoint) * 2) + 1][i] = markerTarget[1]

            data.to_csv('resources/'+ video_name +'.csv', index=False, header=None)

        if key == ord('l') and i != 0:
            i = i - 1

        if key == ord('k') and i != frame_count:
            i = i + 1

        if key == ord('q'):
            break
    else:
        break


'Releasrelease everything'
capture.release()
cv.destroyAllWindows()
