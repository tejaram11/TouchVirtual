# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 23:24:53 2023

@author: TEJA
"""

import cv2
import mediapipe as mp
import time
import pyautogui
pyautogui.FAILSAFE=False



hands= mp.solutions.hands.Hands()
drawing_obj=mp.solutions.drawing_utils


class detector():
    def __init__(self):
        self.cap=cv2.VideoCapture(0)
        
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        
    def hand_detector(self):
        screen_w, screen_h= pyautogui.size()
        index_x,index_y,thumb_x,thumb_y,mid_x,mid_y=0,0,0,0,0,0
        success, frame=self.cap.read()
        frame=cv2.flip(frame,1)
        time_start=0
        time_end=0
        self.roi_w=600
        self.roi_h=400
        self.roi_x=25
        self.roi_y=35
        #extracting ROI
        frameRGB=frame[self.roi_y:self.roi_y+self.roi_w,self.roi_x:self.roi_x+self.roi_h]
        frameRGB=cv2.cvtColor(frameRGB,cv2.COLOR_BGR2RGB)
        frame_h,frame_w,_=frameRGB.shape
        results=hands.process(frameRGB).multi_hand_landmarks
        
        
        
        if results:
            for hand_coord in results:
                landmarks=hand_coord.landmark
                #(hand_coord.landmark)['x']+=x
                #(hand_coord.landmark)['roi_y']+=y
                
                #drawing_obj.draw_landmarks(frame, hand_coord)
                #print(hand_coord)
                
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x*self.roi_w)#+self.roi_x
                    y = int(landmark.y*self.roi_h)#+self.roi_y
                    print(x, y)
                    if id == 8:
                                              
                        index_x = screen_w/frame_w*x
                        index_y = screen_h/frame_h*y
                        pyautogui.moveTo(index_x,index_y,0.2)
                        
                        cv2.circle(img=frame, center=(x,y), radius=9, color=(0,255,255))
                    if id == 4:
                        
                        thumb_x = screen_w/frame_w*x
                        thumb_y = screen_h/frame_h*y
                        print('outside ',abs(index_y - thumb_y))
                        if abs(index_y - thumb_y)<5 or abs(index_x - thumb_x)<5:
                            pyautogui.click(index_x,index_y,button="right")
                            pyautogui.sleep(1)
                            cv2.putText(frame, "click", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0,255), 2)
                        cv2.circle(img=frame, center=(x,y), radius=5, color=(0,0,255))
                    if id == 12:
                        
                        mid_x = screen_w/frame_w*x
                        mid_y = screen_h/frame_h*y
                        print('outside ',abs(index_y - mid_y))
                        if abs(index_y - mid_y)<5 or abs(index_x - mid_x)<5:
                            pyautogui.click(index_x,index_y)
                            pyautogui.sleep(1)
                            cv2.putText(frame, 'leftclick', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.circle(img=frame, center=(x,y), radius=5, color=(0,255,0))
                
                
                
        time_start=time.time()
        fps=1/(time_start-time_end)
        time_end = time_start
        
        cv2.rectangle(frame,(self.roi_x,self.roi_y),(self.roi_x+self.roi_w,self.roi_y+self.roi_h),(255,0,0),3)
        
        _,jpg=cv2.imencode('.jpg',frame)
        
        return jpg.tobytes()