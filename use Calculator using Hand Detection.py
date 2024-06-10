import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time
class game:
    def __init__(self,pos,hi,we,val):
        self.pos = pos
        self.we = we
        self.hi = hi
        self.val = val

    def draw(self,img):
        cv2.rectangle(img,self.pos,(self.pos[0]+self.we,self.pos[1]+self.hi),(255,255,255),-1)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.we, self.pos[1] + self.hi), (55, 55, 55), 3)
        cv2.putText(img,self.val,(self.pos[0]+40,self.pos[1]+50),3,1,(0,0,0),2)

    def cheak(self,x,y):
        if self.pos[0] < x < self.pos[0]+self.we and self.pos[1] < y < self.pos[1]+self.hi:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.we, self.pos[1] + self.hi), (255, 255, 255), -1)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.we, self.pos[1] + self.hi), (55, 55, 55), 3)
            cv2.putText(img, self.val, (self.pos[0] + 20, self.pos[1] + 50), 3, 2, (0, 0, 0), 5)
            return True
        else:
            return False

cap = cv2.VideoCapture(0)
cap.set(3,1000)
cap.set(4,1000)


char = [['7','8','9','+','clr'],
               ['4','5','6','-'],
               ['1','2','3','*'],
               ['0','/','.','=']
               ]


detector = HandDetector(maxHands=1)
bList =[]
for i in range(4):
    for j in range(4):
       x = i*80 + 50
       y = j*80 + 200
       bList.append(game((x,y),80,80,char[j][i]))





equ = ""
c=0
while True:
    ret,img = cap.read()
    img = cv2.flip(img,1)
    #imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    hands, img = detector.findHands(img,True)

    cv2.rectangle(img, (50, 140), (320 + 50, 200), (255, 255, 255), -1)
    cv2.rectangle(img, (50, 140), (320 + 50, 200), (55, 55, 55), 5)
    cv2.rectangle(img,(370,140),(370+80,130+70),(255,255,255),-1)
    cv2.rectangle(img, (370, 140), (370 + 80, 140 + 60), (55, 55, 55), 3)
    cv2.putText(img,"clr",(380,170),3,1,(55,55,55),3)
    cv2.rectangle(img,(370+80,140 + 60),(370,170+80+80+80+80+30),(255,255,255),-1)
    cv2.rectangle(img, (370 + 80, 140 + 60), (370, 170 + 80 + 80 + 80 + 80+30), (55, 55, 55), 3)
    cv2.putText(img,"HIMEL",(20,30),3,1,(255,0,0),2)

    for i in bList:
        i.draw(img)
    if hands:
        lmlist = hands[0]['lmList']
        s = lmlist[8]
        sx, sy = s[0], s[1]
        cv2.circle(img, (sx, sy), 10, (255, 0, 0), -1)
        m = lmlist[12]
        mx, my = m[0], m[1]
        cx, cy = (sx + mx) // 2, (sy + my) // 2
        cv2.circle(img, (mx, my), 10, (255, 0, 0), -1)
        cv2.line(img, (sx, sy), (mx, my), (255, 0, 0), 2)
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), -1)

        dis = np.hypot(mx-sx,my-sy)



        if dis<=40:
            for i,button in enumerate(bList):
                if button.cheak(sx,sy):
                    val = char[int(i%4)][int(i/4)]
                    if val=='=':
                        equ=str(eval(equ))
                    else:
                        equ+=val
                    time.sleep(.2)

        if dis<=50:
            if 370 <sx < 370+80 and 140 <sy <140+60:
                equ=""







    cv2.putText(img, equ, (60, 180), 3, 1, (55, 55, 55), 3)

    cv2.imshow("Img",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


#himel11
