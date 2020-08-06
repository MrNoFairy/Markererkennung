import numpy as np
import colorsys as colorsys
import cv2 as cv
'''-------------------------------------------------------------------------------------
Colorspace Functions
-------------------------------------------------------------------------------------'''

'''
Problem 1 : Different applications use different scales for HSV.
For example gimp uses H = 0-360, S = 0-100 and V = 0-100. But OpenCV uses H: 0-179, S: 0-255, V: 0-255.

Problem 2 : Different Functions uses different Colorspaces
Used Colorspaces are RGB, GRB, HSV, CVHSV (opencv HSV) but mainly GRB & CVHSV
'''

#TODO major CVHSV2BGR
#TODO minor RGB2HSV, HSV2RGB, GBR2HSV, HSV2GBR, RGB2CVHSV, CVHSV2RGB

def HSV2CVHSV(hue, saturation, value):
    hue = round(hue/360*179)
    saturation = round(saturation/100*255)
    value = round(value/100*255)
    return hue, saturation, value

def CVHSV2HSV(hue, saturation, value):
    hue = round(hue/179*360)
    saturation = round(saturation/255*100)
    value = round(value/255*100)
    return hue, saturation, value

def RGB2BGR(r, g, b):
    return b, g, r

def BGR2RGB(b, g, r):
    return r, g, b

def BGR2CVHSV(b, g, r):

    b, g, r = b / 255.0, g / 255.0, r / 255.0
    cmax = max(b, g, r)
    cmin = min(b, g, r)
    diff = cmax - cmin

    if cmax == cmin:
        h = 0
    elif cmax == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360

    if cmax == 0:
        s = 0
    else:
        s = (diff / cmax) * 100

    v = cmax * 100

    h = round(h / 360 * 179)
    s = round(s / 100 * 255)
    v = round(v / 100 * 255)

    return h, s, v

def BGR2CVHSV(b, g, r):

    b, g, r = b / 255.0, g / 255.0, r / 255.0
    cmax = max(b, g, r)
    cmin = min(b, g, r)
    diff = cmax - cmin

    if cmax == cmin:
        h = 0
    elif cmax == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360

    if cmax == 0:
        s = 0
    else:
        s = (diff / cmax) * 100

    v = cmax * 100

    h = round(h / 360 * 179)
    s = round(s / 100 * 255)
    v = round(v / 100 * 255)

    return h, s, v


def HSV2RGB(h, s, v):
    h, s, v = h / 179.0, s / 255.0, v / 255.0
    if s == 0.0: v *= 255; return (v, v, v)
    i = int(h * 6.)  # XXX assume int() truncates!
    f = (h * 6.) - i;
    p, q, t = int(255 * (v * (1. - s))), int(255 * (v * (1. - s * f))), int(255 * (v * (1. - s * (1. - f))));
    v *= 255;

    v = round(v)
    t = round(t)
    p = round(p)
    q = round(q)

    i %= 6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

'''-------------------------------------------------------------------------------------
Functions
-------------------------------------------------------------------------------------'''

'''
Problem 1 : 
'''

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx #array[idx]

def decode_fourcc(fourcc):
    ''' Decodes the fourcc value to get the four chars identifying it
    by Opencv 4 with python site 97
    '''
    fourcc_int = int(fourcc)

    #asdf
    fourcc_decode = ""
    for i in range(4):
        int_value = fourcc_int >> 8 * i & 0xFF
        fourcc_decode += chr(int_value)
    return fourcc_decode

def blurandthresh(img, thresh, value):
    img = cv.GaussianBlur(img, value, 0)
    img = cv.threshold(img, thresh, 255, cv.THRESH_BINARY)[1]
    return img