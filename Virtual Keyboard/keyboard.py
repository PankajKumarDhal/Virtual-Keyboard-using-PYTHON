import cv2
import cvzone
from HandTrackingModule import handDetector as HandDetector
from PyQt5 import QtWidgets, QtGui

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P","&"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";","%"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/","?"],
        ["9", "8", "7", "6", "5", "4", "3", "2", "1", "0","clear"]]
finalText = ""
# print(type(finalText))

def drawALL(img, buttonList):

  for button in buttonList:
    x, y = button.pos

    w, h = button.size
    cv2.rectangle(img, button.pos, (x + w, y + h),
                  (255, 0, 0), cv2.FILLED)
    cv2.putText(img, button.text, (x + 20, y + 65),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

  return img




class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text



buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


#myButton = Button([100,100], "A")
#myButton1 = Button([300,100], "B")
#myButton2= Button([500,100], "C")


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawALL(img, buttonList)

    if lmList:
        for button in buttonList:
            x,y = button. pos
            w,h = button.size

            if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h :
                cv2.rectangle(img, button.pos, (x + w, y + h),(1750, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12,img,draw=False)
                print(l)

                ## when clicked
                if l < 24:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0,255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    finalText += button.text
                    if button.text == "clear":
                        finalText=finalText.replace(finalText,"")



    cv2.rectangle(img, (50,500),(1200,600),
                  ( 0,255, 255), cv2.FILLED)
    cv2.putText(img, finalText, (60, 550),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    # for i in range(len(keys)):
    #  for j, key in enumerate(keys[i]):
    #     buttonList.append(Button([100 * j + 50, 100 * i + 50],key))
    #img = myButton.draw(img)
    #img = myButton1.draw(img)
    #img = myButton2.draw(img)

    cv2.imshow("Image", img)
    k = cv2.waitKey(1)