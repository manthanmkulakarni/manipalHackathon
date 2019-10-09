from __future__ import print_function
import cv2 as cv
import argparse
from PIL import Image
import numpy as np

def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect faces
    eye_center=0
    radius=0
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 5)
        faceROI = frame_gray[y:y+h,x:x+w]
        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        i=0
        mouth=[]
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
            im=np.array(frame)
            mouth.append(eye_center[1]-50)
            im=im[eye_center[1]-50:eye_center[1]+50,eye_center[0]-50:eye_center[0]+50]
            cv.imwrite("croppedeye"+str(i)+".jpg",im)
            i=i+1
        im=np.array(frame)
        im=im[mouth[0]:mouth[1],mouth[0]+100:mouth[1]+100]
        cv.imwrite("croppedmouth.jpg",im)
    cv.imwrite('detection.jpg', frame)
    
    
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='haarcascades/haarcascade_eye_tree_eyeglasses.xml')
parser.add_argument('--mouth_cascade', help='Path to eyes cascade.', default='haarcascades/haarcascade_smile.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
mouth_cascade_name = args.mouth_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
mouth_cascade = cv.CascadeClassifier()


#-- 1. Load the cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)
    
if not mouth_cascade.load(cv.samples.findFile(mouth_cascade_name)):
    print('--(!)Error loading mouth cascade')
    exit(0)    
camera_device = args.camera
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

camera = cv.VideoCapture(0)
image=0
while True:
    return_value,image = camera.read()
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    cv.imshow('image',gray)
    if cv.waitKey(1)& 0xFF == ord('s'):
        cv.imwrite('test.jpg',image)
        break
camera.release()
cv.destroyAllWindows()
    
detectAndDisplay(image)

    
