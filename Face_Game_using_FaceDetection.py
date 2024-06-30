import os
import cvzone
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import random
import time

# Set up video capture
cap = cv2.VideoCapture(0)
cap.set(3, 2000)
cap.set(4, 2000)

# Initialize face mesh detector
detector = FaceMeshDetector(maxFaces=1)
lit = [0, 17, 78, 292]

# Load eatable images
folderEatable = 'Kidss/eatable'
listEatable = os.listdir(folderEatable)
eatable = [cv2.imread(f'{folderEatable}/{i}', cv2.IMREAD_UNCHANGED) for i in listEatable]

# Load non-eatable images
foldernonEatable = 'Kidss/noneatable'
listnonEatable = os.listdir(foldernonEatable)
noneatable = [cv2.imread(f'{foldernonEatable}/{i}', cv2.IMREAD_UNCHANGED) for i in listnonEatable]

# Initial object settings
objects = eatable[0]
pos = [200, 0]
speed = 10
count = 0
eat = True
over = False
ti = 30
startime = time.time()

# Function to reset object
def reset():
    global eat
    pos[0] = random.randint(100, 1200)
    pos[1] = 0
    if random.randint(0, 2) == 0:
        objects = noneatable[random.randint(0, len(noneatable) - 1)]
        eat = False
    else:
        objects = eatable[random.randint(0, len(eatable) - 1)]
        eat = True
    return objects, pos

while True:
    ret, img = cap.read()
    if not ret:
        break

    if time.time() - startime < ti:
        if not over:
            img = cv2.flip(img, 1)
            img, faces = detector.findFaceMesh(img, draw=False)
            img = cvzone.overlayPNG(img, objects, pos)
            pos[1] += speed

            if pos[1] > 650:
                objects, pos = reset()

            if faces:
                face = faces[0]
                for id in lit:
                    cv2.circle(img, face[id], 5, (255, 0, 255), -1)

                cv2.line(img, face[lit[0]], face[lit[1]], (255, 0, 0), 3)
                cv2.line(img, face[lit[2]], face[lit[3]], (255, 0, 0), 3)

                ver, _ = detector.findDistance(face[lit[0]], face[lit[1]])
                hori, _ = detector.findDistance(face[lit[2]], face[lit[3]])
                ratio = (ver / hori) * 100

                up = face[lit[0]]
                down = face[lit[1]]
                cx, cy = (up[0] + down[0]) // 2, (up[1] + down[1]) // 2
                cv2.line(img, (cx, cy), (pos[0] + 50, pos[1] + 50), (255, 0, 0), 3)
                dis, _ = detector.findDistance((cx, cy), (pos[0] + 50, pos[1] + 50))

                if ratio <= 60:
                    cv2.putText(img, "closed", (50, 50), 2, 2, (255, 0, 0), 2)
                else:
                    cv2.putText(img, "open", (50, 50), 3, 2, (255, 0, 0), 2)

                if dis <= 300 and ratio >= 60:
                    if eat:
                        objects, pos = reset()
                        count += 1
                    else:
                        over = True

            cvzone.putTextRect(img, f'Score: {count}', (1050, 130), scale=3)
            cvzone.putTextRect(img, f'Time: {int(ti - (time.time() - startime))}', (1050, 70), scale=3)
        else:
            cv2.putText(img, f'Score: {count}', (300, 200), 5, 5, (55, 55, 55), 5)
            cv2.putText(img, "Game Over", (300, 400), 5, 5, (55, 55, 55), 5)
            cv2.putText(img, "r for restart", (300, 500), 5, 5, (55, 55, 55), 5)
            cv2.putText(img, "q for quit", (300, 600), 5, 5, (55, 55, 55), 5)
            cv2.putText(img, "Made by Himel", (300, 700), 2, 2, (55, 55, 55), 4)
    else:
        cv2.putText(img, f'Score: {count}', (300, 200), 5, 5, (55,55, 55), 5)
        cv2.putText(img, "Game Over", (300, 400), 5, 5, (55, 55, 55), 5)
        cv2.putText(img, "r for restart", (300, 500), 5, 5, (55, 55, 55), 5)
        cv2.putText(img, "q for quit", (300, 600), 5, 5, (55, 55, 55), 5)
        cv2.putText(img, "Made by Himel", (300, 700), 2, 2, (55, 55, 55), 4)

    cv2.imshow("Img", img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        objects, pos = reset()
        over = False
        count = 0
        startime = time.time()
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
