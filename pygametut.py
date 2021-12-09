import pygame
import cv2
import mediapipe as mp
import time
import numpy as np
from pynput.keyboard import Key, Controller
pygame.init()
win=pygame.display.set_mode([600,600])
pygame.display.set_caption("First Game")
path='C:/Users/sweet/Desktop/Shreya/books/sem7/final year/ASSETS/character/'
walkRight = [pygame.image.load(path+'R1.png'), pygame.image.load(path+'R2.png'), pygame.image.load(path+'R3.png'), pygame.image.load(path+'R4.png'), pygame.image.load(path+'R5.png'), pygame.image.load(path+'R6.png'), pygame.image.load(path+'R7.png'), pygame.image.load(path+'R8.png'), pygame.image.load(path+'R9.png')]
walkLeft = [pygame.image.load(path+'L1.png'), pygame.image.load(path+'L2.png'), pygame.image.load(path+'L3.png'), pygame.image.load(path+'L4.png'), pygame.image.load(path+'L5.png'), pygame.image.load(path+'L6.png'), pygame.image.load(path+'L7.png'), pygame.image.load(path+'L8.png'), pygame.image.load(path+'L9.png')]
bg = pygame.image.load(path+'bg.jpg')
char = pygame.image.load(path+'standing.png')

x=50
y=300
width=40
height=60
jx=20
jy=250
fx=580
fy=250
vel=5
screen_width=600
cap = cv2.VideoCapture(0)
joint_list =[[8,5,0]]   
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
Jump=False
Jcnt=10
run=True
keyboard=Controller()
walkCount=0
left = False
right = False
Fast=False
def redrawGameWindow():
    global walkCount
    
    win.blit(bg, (0,0))  
    if walkCount + 1 >= 27:
        walkCount = 0
        
    if left:  
        win.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1                          
    elif right:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    else:
        win.blit(char, (x, y))
        walkCount = 0
        
    pygame.display.update() 
while run:
    pygame.time.delay(100)
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    x1, y1 = 0, 200
    x2, y2 = 800,200
    line_thickness = 2
    cv2.line(img, (x1, y1), (x2, y2), (0, 200, 0), thickness=line_thickness)
    x1, y1 = 0, 300
    x2, y2 = 800,300
    cv2.line(img, (x1, y1), (x2, y2), (0, 300, 0), thickness=line_thickness)
    cv2.circle(img, (jx,jy), 40, (0,0,255), 2)
    cv2.circle(img, (fx,fy), 40, (0,0,255), 2)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                # cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)
                # cv2.putText(img,str(cx), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
            # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            cv2.circle(img, (cx,cy), 3, (0,0,255), cv2.FILLED)
            cv2.circle(img, (800, 800), 30, (255,0,0), cv2.FILLED)
            if (cx - fx)**2 + (cy - fy)**2 < 40*40:
                
                Fast=True
                             
                cv2.putText(img,ud, (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
                print("Fast",cy)
            if (cx - jx)**2 + (cy - jy)**2 < 40*40:
                ud="Jump"
                Jump=True
                keyboard.press(Key.space)
                
                cv2.putText(img,ud, (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
                print("JUmp",cy)
           

            elif cy<200:
                ud="Up"
                keyboard.press(Key.up)
                
                cv2.putText(img,ud, (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
                print("Up",cy)
                
            elif cy>300:
                ud="Down"
                keyboard.press(Key.down)
                
                cv2.putText(img,ud, (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
                print("Down",cy)
        for hand in results.multi_hand_landmarks:
        # Loop through joint sets
            for joint in joint_list:
                a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])  # First coord
                b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])  # Second coord
                c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y])  # Third coord
                radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                angle = np.abs(radians * 180.0 / np.pi)
                cv2.putText(img, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                if angle<=60 and angle>=40:
                    print("")
                elif angle<=130:
                    direction="Right"
                    keyboard.press(Key.right)
                    
                    # cv2.putText(img, "Right", (30,30),
                    #     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(img,direction, (500,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
                else:
                    direction="Left"
                    keyboard.press(Key.left)
                    
                    # cv2.putText(img, "Left", (30,30),
                    #     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(img,direction, (500,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
                    print("Left")  
                          
    # cTime = time.time()
    # fps = 1/(cTime-pTime)
    # pTime = cTime
    # cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    for event in pygame.event.get():
      if event.type== pygame.QUIT:
          run=False
    keys=pygame.key.get_pressed()
    if Fast:
        vel=15
    if keys[pygame.K_LEFT] and x>vel:
            x-=vel
            left = True
            right = False
            print(vel)
            keyboard.release(Key.left)
            Fast=False
            vel=5
    elif keys[pygame.K_RIGHT] and x<screen_width-width-vel:
            x += vel
            left = False
            right = True
            print(vel)
            keyboard.release(Key.right)
            Fast=False
            vel=5
  
    else: 
        left = False
        right = False
        walkCount = 0
        Fast=False
        vel=5
    if not Jump:
        if keys[pygame.K_UP] and y>vel:
                y-=vel
                keyboard.release(Key.up)
        if keys[pygame.K_DOWN] and y<screen_width-height-vel:
                y+=vel
                keyboard.release(Key.down)
        if keys[pygame.K_SPACE]:
            Jump=True
            left = False
            right = False
            walkCount = 0
    else:
        if Jcnt>= -10:
            neg=1
            if Jcnt<0:
                neg=-1
            y-= ((Jcnt)**2)*0.5*neg
            Jcnt-=1
        else:
            Jump=False
            Jcnt=10
        keyboard.release(Key.space)
    win.fill((0,0,0))
    redrawGameWindow()
    
            
    # pygame.draw.rect(win, (255,0,0), (x,y,width, height))
    # pygame.display.update()
    # pygame.time.delay(100)
    # print("am here")
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    
          
pygame.quit()