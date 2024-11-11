# [ScaleWidth, ScaleHeight] = windowSize()
# SectionSizes = retreiveSectionSizes()

import cv2
from pyzbar import pyzbar
import ctypes

def cameraSource():
    return 0

def windowSize():
    return [1366, 7488]


# 1536 x 1024 (0.9,0.96,0.9)
# 1920 x 1080 (1.3,1.3,1.2)


user32 = ctypes.windll.user32
screensizex, screensizey = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# print(screensizex)
# print(screensizey)

scaleSizex = 1.3 * (screensizex / 1920)
scaleSizey = 1.3 * (screensizey / 1080)
scaleF = 1.2 * (screensizex / 1920)


def retIntList2(list):
    tempa = int(list[0] * scaleSizex)
    tempb = int(list[1] * scaleSizey)
    return [tempa, tempb]


def retIntList4(list):
    tempa = int(list[0] * scaleSizex)
    tempb = int(list[1] * scaleSizey)
    tempc = int(list[2] * scaleSizex)
    tempd = int(list[3] * scaleSizey)
    return [tempa, tempb, tempc, tempd]


def retIntImg4(list):
    tempa = int(list[0] * scaleSizex)
    tempb = int(list[1] * scaleSizey)
    tempc = int(list[2] * scaleSizex)
    tempd = int(list[3] * scaleSizey)
    tempe = max(tempc, tempd)
    return [tempa, tempb, tempe, tempe]


def retreiveSectionSizes():
    dic = {"header": [], "sidebar": [], "bodyframe1": [], "bodyframe2": [], "bodyframe3": [], "bodyframe4": []
           , "cameraframe": []}
    dic["header"] = retIntList2([1070, 40])
    dic["sidebar"] = retIntList2([300, 750])
    dic["bodyframe1"] = retIntList2([1040, 350])
    dic["bodyframe2"] = retIntList4([310, 235, 150, 25])
    dic["bodyframe3"] = retIntList2([310, 235])
    dic["bodyframe4"] = retIntList2([310, 235])
    dic["cameraframe"] = retIntList2([480, 320])

    return dic


# self.SectionSizes["header"]=[1070,60]
# self.SectionSizes["sidebar"]=[300,750]
# self.SectionSizes["bodyframe1"]=[1040,350]
# self.SectionSizes["bodyframe2"]=[310,235]
# self.SectionSizes["bodyframe3"]=[310,235]
# self.SectionSizes["bodyframe4"]=[310,235]


def retreiveSectionLoc():
    dic = {"header": [], "exit": [], "sidebar": [], "heading": [], "bodyframe1": [], "bodyframe2": [],
           "bodyframe3": [], "bodyframe4": [], "logo": [], "brandName": [], "dashboard": [], "dashboardText": [],
           "summary": [], "save": [], "refresh": [], "records": [], "trayLevels": [], "itemframes": [], "itemSel": [],
           "addIm": [], "alert": [], "read": [], "readBut": [],"registerUN":[],"registerUid":[],"getUid":[]}
    dic["header"] = retIntList2([int(1366 * 0.22), 0])
    dic["exit"] = retIntList2([1010, 6])
    dic["sidebar"] = retIntImg4([0, 0, 25, 25])
    dic["heading"] = retIntList2([int(1366 * 0.23), 70])
    dic["bodyframe1"] = retIntList2([328, 110])
    dic["bodyframe2"] = retIntList4([int(1366 * 0.24), int(7488 * 0.068), int(1366 * 0.24) + 2, int(7488 * 0.068) - 30])
    dic["bodyframe3"] = retIntList2([int(1366 * 0.505), int(7488 * 0.068)])
    dic["bodyframe4"] = retIntList2([int(1366 * 0.77), int(7488 * 0.068)])
    dic["logo"] = retIntImg4([120, 80, 51, 51])
    dic["brandName"] = retIntList2([80, 150])
    dic["dashboard"] = retIntList2([38, 287])
    dic["dashboardText"] = retIntList2([81, 289])
    dic["summary"] = retIntList4([38, 337, 79, 339])
    dic["save"] = retIntList4([38, 387, 80, 389])
    dic["refresh"] = retIntList4([38, 437, 79, 439])
    dic["trayLevels"] = retIntList2([15, 10])
    dic["itemframes"] = [retIntList4([45, 70, 200, 120]), retIntList4([295, 70, 200, 120]),
                         retIntList4([545, 70, 200, 120]), retIntList4([795, 70, 200, 120]),
                         retIntList4([45, 210, 200, 120]), retIntList4([295, 210, 200, 120]),
                         retIntList4([545, 210, 200, 120]), retIntList4([795, 210, 200, 120])]
    dic["itemSel"] = retIntList2([330, 479])
    dic["records"] = retIntList4([38, 487, 79, 489])
    dic["addIm"] = retIntList2([15, 15])
    dic["alert"] = retIntImg4([158, 337, 12, 12])
    dic["read"] = retIntList4([70, 155, 130, 26])
    dic["readBut"] = retIntList2([70, 157])
    dic["registerUN"] = retIntList2([650, 100])
    dic["registerUid"] = retIntList2([800, 100])
    dic["getUid"] = retIntList2([800, 135])
    return dic


def retrievefontSizes():
    a = [int(12 * scaleF), int(13 * scaleF), int(15 * scaleF), int(20 * scaleF), int(9), int(10), int(16 * scaleF)]
    return a


def retrieveColors():
    dic = {"window": [], "header": [], "exit": [], "sidebar": [], "heading": [],
           "bodyframe1": [], "bodyframe2": [], "bodyframe3": [], "bodyframe4": [], "white": [], "black": [],
           "itemframe": [], "green": [], "orange": [], "grey": []}
    dic["window"] = ['#eff5f6']
    dic["header"] = ['#064789']
    dic["exit"] = ['#D2001A', '#0A8754']
    dic["sidebar"] = ['#ffffff']
    dic["heading"] = ['#0064d3', '#eff5f6']
    dic["bodyframe1"] = ['#ffffff']
    dic["bodyframe2"] = ['#A2B5BB', '#eff5f6']
    dic["bodyframe3"] = ['#A2B5BB']
    dic["bodyframe4"] = ['#A2B5BB']
    # dic["bodyframe2"] = ['#82AAE3','#eff5f6']
    # dic["bodyframe3"] = ['#CE7777']
    # dic["bodyframe4"] = ['#DEA47E']
    dic["white"] = ['#ffffff']
    dic["black"] = ['#000000']
    dic["itemframe"] = ['#E1E8EB']
    dic["green"] = ['#50C878']
    dic["orange"] = ['#F28C28']
    dic["grey"] = ['#f0f0f0']
    return dic
