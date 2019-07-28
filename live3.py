from __future__ import print_function
import cv2 as cv
import argparse
#available fourcc codecs:http://www.fourcc.org/codecs.php
#fourcc = cv.VideoWriter_fourcc(*'XVID')
fourcc = cv.VideoWriter_fourcc(*'X264')
#out = cv.VideoWriter('output.avi',fourcc, 20.0, (640,480))
out = cv.VideoWriter('output.mkv',fourcc,5.0, (640,480)) #changed from 20.0 to 5.0 - seemed smoother

def detectAndDisplay(frame):
    eyeCoord=''
    faceColor=(0,255,0)
    eyeColor=(0,0,255)
    fontColor=(255,255,255)
    font=cv.FONT_HERSHEY_SIMPLEX
    fontPosition = (10,10)
    eyePosition = (20,15)
    fontScale              = .5
    lineType               = 2
    #create a video writer
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    fc=0
    for (x,y,w,h) in faces:
        fc=fc+1
        center = (x + w//2, y + h//2)
#cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#change face to rectangle
#        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        frame = cv.rectangle(frame, (x, y), (x+w, y+h), faceColor, 1)
        fontPosition=(x-20,y)
        #eyePosition=(x,y+h)
        faceROI = frame_gray[y:y+h,x:x+w]
        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        offset="    "
        ect=0;
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            e1=x + x2 + w2//2
            e2=y + y2 + h2//2
            eyeCoord='Eyes:{0} {1}'.format(eye_center,e1-e2)
            print (eyeCoord)
            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, eyeColor, 1)
    ovl ="Tracking:{0}".format(fc)
    evl = " {0}".format(eyeCoord)
    cv.putText(frame,ovl,fontPosition,font,fontScale,fontColor,lineType)
    cv.putText(frame,eyeCoord,eyePosition,font,fontScale,fontColor,lineType)
    cv.imshow('Capture - Face detection', frame)
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='/home/pi/bin/opencv/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='home/pi/bin/opencv/haarcascade_eye_tree_eyeglasses.xml')
parser.add_argument('--camera', help='Camera devide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
#-- 1. Load the cascades
#if not face_cascade.load('/home/pi/bin/opencv/haarcascade_fullbody.xml'):
if not face_cascade.load('/home/pi/bin/opencv/haarcascade_frontalface_alt.xml'):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load('/home/pi/bin/opencv/haarcascade_eye_tree_eyeglasses.xml'):
    print('--(!)Error loading eyes cascade')
    exit(0)
camera_device = args.camera
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    out.write(frame)
    if cv.waitKey(10) == 27:
        break