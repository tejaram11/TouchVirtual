# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 13:59:32 2023

@author: TEJA
"""

import cv2
import mediapipe as mp
import time
import pyautogui
pyautogui.FAILSAFE=False

hands= mp.solutions.hands.Hands(model_complexity=1)
drawing_obj=mp.solutions.drawing_utils
screen_w, screen_h= pyautogui.size()
index_x,index_y,thumb_x,thumb_y,mid_x,mid_y=0,0,0,0,0,0

class detector():
    
    def configure_screen(self):
        self.cap=cv2.VideoCapture(2) #2 for external camera, 0 for inbuilt webcam
        success, frame=self.cap.read()
        #frame=cv2.flip(frame,1)
        self.roi_x,self.roi_y,self.roi_w,self.roi_h=cv2.selectROI("select the area",frame)
        
        
    def touch_detect(self):
     screen_w, screen_h= pyautogui.size()
     index_x,index_y,thumb_x,thumb_y,mid_x,mid_y=0,0,0,0,0,0
     while True:
        success, frame=self.cap.read()
        frame=cv2.flip(frame,0)
        time_start=0
        time_end=0
    
        #extracting ROI
        #frameRGB=frame[self.roi_y:self.roi_y+self.roi_w,self.roi_x:self.roi_x+self.roi_h]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame_h,frame_w,_=frameRGB.shape
        frame.flags.writeable=False
        results=hands.process(frameRGB).multi_hand_landmarks #detecting hands from frame
        frame.flags.writeable=True
        
        
        
        if results:
            for hand_coord in results:
                landmarks=hand_coord.landmark #extracting coordinates from detection
                #(hand_coord.landmark)['x']+=x
                #(hand_coord.landmark)['roi_y']+=y
                
                #drawing_obj.draw_landmarks(frame, hand_coord)
                #print(hand_coord)
                
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x*frame_w) #calculating the original coordinates of screen from relative coordinates
                    y = int(landmark.y*frame_h)
                    print(x, y)
                    if id == 8: #for index finger
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255))                      
                        index_x = screen_w/frame_w*x
                        index_y = screen_h/frame_h*y
                        pyautogui.moveTo(index_x,index_y,0.2)
                        pyautogui.sleep(1)
                    if id == 4: #for thumb
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255))
                        thumb_x = screen_w/frame_w*x
                        thumb_y = screen_h/frame_h*y
                        print('outside ',abs(index_y - thumb_y))
                        if abs(index_y - thumb_y)<20:
                            pyautogui.click(button='right')
                            pyautogui.click(clicks=2)
                            pyautogui.sleep(1)
                    if id == 12: #for middle finger
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255))
                        mid_x = screen_w/frame_w*x
                        mid_y = screen_h/frame_h*y
                        print('outside ',abs(index_y - mid_y))
                        if abs(index_y - mid_y)<20:
                            pyautogui.click(button='left')
                            pyautogui.click(clicks=2)
                            pyautogui.sleep(1)
                
                
                
        time_start=time.time()
        fps=1/(time_start-time_end)
        time_end = time_start
        
        cv2.rectangle(frame,(self.roi_x,self.roi_y),(self.roi_x+self.roi_w,self.roi_y+self.roi_h),(255,0,0),3)
        cv2.imshow("image",frame)
        key = cv2.waitKey(500) & 0xFF
        if key == ord('q'):
            break
        
        
     self.cap.release()
     cv2.destroyAllWindows()
        
        
        #_,jpg=cv2.imencode('.jpg',frame)
        #return jpg.tobytes()
    
    def start(self):
    
        test_det=detector()
        detector.configure_screen(test_det)
        detector.touch_detect(test_det)
        
        
test_det=detector()
detector.configure_screen(test_det)
detector.touch_detect(test_det)
        