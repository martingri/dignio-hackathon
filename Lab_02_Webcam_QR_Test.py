# -*- coding: utf-8 -*-
"""
Created on Tue Oct 7 11:41:42 2018

@author: Caihao.Cui
"""
from __future__ import print_function

from tkinter import END, CENTER, ALL, SEL_LAST, SEL_FIRST

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
import tkinter as tk
import tkinter.font as tkFont

gui = tk.Tk()
gui.geometry("1920x1080")
text = tk.Text(gui, height=100, width=150)
text.pack()
myFont = tkFont.Font(family="Times New Roman", size=200, weight="bold", slant="italic")
text.configure(font = myFont)
text.insert(END, "Atuin is ready")
text.update()
# get the webcam:
cap = cv2.VideoCapture(4)

cap.set(3,640)
cap.set(4,480)
#160.0 x 120.0
#176.0 x 144.0
#320.0 x 240.0
#352.0 x 288.0
#640.0 x 480.0
#1024.0 x 768.0
#1280.0 x 1024.0
time.sleep(2)

import serial
import time
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
def write(signal):
    print("printing ")
    arduino.write(bytes(signal, 'utf-8'))

def decode(im) :
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')     
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

qr_value = ""

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         
    decodedObjects = decode(im)
    for decodedObject in decodedObjects:
        points = decodedObject.polygon
     
        # If the points do not form a quad, find convex hull
        if len(points) > 4 : 
          hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
          hull = list(map(tuple, np.squeeze(hull)))
        else : 
          hull = points;
         
        # Number of points in the convex hull
        n = len(hull)     
        # Draw the convext hull
        for j in range(0,n):
          cv2.line(frame, hull[j], hull[ (j+1) % n], (255,0,0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        print(x, y)

        print('Type : ', decodedObject.type)
        print('Data : ', decodedObject.data,'\n')
        print(f"qr value {qr_value}")
        if qr_value == decodedObject.data:
            continue
        qr_value = decodedObject.data
        barCode = str(decodedObject.data)
        cv2.putText(frame, barCode, (x, y), font, 1, (0,255,255), 2, cv2.LINE_AA)
        text.delete("1.0", "end")
#        text.quit()
        text.insert(END, qr_value)
        gui.update()
        time.sleep(2)
        if(qr_value == b'3 Ibuprofen\n2 TicTac\n'):
            write("01001010011")
        elif(qr_value == b'2 Asprin\n4 TicTac\n'):
            write("2")
        else:
            write("3")

    # Display the resulting frame
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'): # wait for 's' key to save 
        cv2.imwrite('Capture.png', frame)     

# When everything done, release the capture
cap.release()
#cv2.destroyAllWindows()



