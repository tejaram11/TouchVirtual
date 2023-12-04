# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 00:05:46 2023

@author: TEJA
"""

import cv2
import mediapipe as mp
import time


hands= mp.solutions.hands.Hands(False,1)
drawing_obj=mp.solutions.drawing_utils

frame_0=True
time_start=0
time_end=0

cap=cv2.VideoCapture(0)


while True:
    success, frame=cap.read()
    frame=cv2.flip(frame,1)
    
    if frame_0:    
        frameROI=cv2.selectROI("select the area",frame)
        frame_0=False
    
    
    frameRGB=frame[int(frameROI[1]):int(frameROI[1]+frameROI[3]),int(frameROI[0]):int(frameROI[0]+frameROI[2])]
    frameRGB=cv2.cvtColor(frameRGB,cv2.COLOR_BGR2RGB)
    results=hands.process(frameRGB).multi_hand_landmarks
    
    
    
    if results:
        for hand_coord in results:
            drawing_obj.draw_landmarks(frame, hand_coord)
            print(hand_coord)
            
    #for calculating fps
    time_start=time.time()
    fps=1/(time_start-time_end)
    time_end = time_start
    
    cv2.putText(frame,str(int(fps)),(15,50),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)
    cv2.imshow("image",frame)
    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
