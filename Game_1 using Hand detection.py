import random
import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import time

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)  # Height

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Find Function
# x is the raw distance, y is the value in cm
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coeff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C

# Game Variables
cx, cy = 250, 250
color = (0,0,255)#(194,66,245)
counter = 0
score = 0
timeStart = time.time()
totalTime = 30 # initial time 30 second

# Main Loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if time.time() - timeStart < totalTime:
        hands, img = detector.findHands(img, draw=False)

        if hands:
            lmList = hands[0]['lmList']
            x, y, w, h = hands[0]['bbox']
            x1, y1 = lmList[5][:2]
            x2, y2 = lmList[17][:2]

            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
            A, B, C = coeff
            distanceCM = A * distance ** 2 + B * distance + C

            if distanceCM < 40:
                if x < cx < x + w and y < cy < y + h:
                    counter = 1
            cv2.rectangle(img, (x, y), (x + w, y + h), (66,126,245), 3)
            cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x + 100, y))

        if counter:
            counter += 1
            color = (44,245,88)
            if counter == 3:
               cx = random.randint(100, 1100)
               cy = random.randint(100, 600)
               color = (0,0,255)
               score += 1
               counter = 0

        # Draw Target
        cv2.circle(img, (cx, cy), 15, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 5, (255,255,255), cv2.FILLED)



        # Game HUD
        cvzone.putTextRect(img, f'Time: {int(totalTime - (time.time() - timeStart))}',
                           (1000, 75), scale=3)
        cvzone.putTextRect(img, f'Score: {str(score).zfill(2)}', (60, 75), scale=3, offset=20)
    else:
        cvzone.putTextRect(img, 'Game Over', (400, 400), scale=5, offset=30, thickness=6)
        cvzone.putTextRect(img, f'Score: {score}', (400, 500), scale=3)
        cvzone.putTextRect(img, 'Press r to restart', (400, 575), scale=2)
        cvzone.putTextRect(img, 'Press q to Leave', (400, 630), scale=2)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        timeStart = time.time()
        score = 0
    if key & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
#himel11
