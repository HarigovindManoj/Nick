import face_recognition
import cv2
import numpy as np
from engine.command import speak
import run

video = cv2.VideoCapture(0)

face  =  face_recognition.load_image_file("c:path where pic is:ninte pic itteku")
faceencoding = face_recognition.face_encoding(face)[0]

face_encodings_list = [
    faceencoding]

face_encodings = []
s  = True
face_coordinates = []

while True:
    speak('Detecting for face')
    _,frame = video.read()

    resized_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    resized_frame_rgb = resized_frame[:,:,::-1]

    if s:
        face_coordinates = face_recognition.face_locations(resized_frame_rgb)
        face_encodings = face_recognition.face_encodings(resized_frame_rgb,face_coordinates)

        for faces in face_encodings:
            matches = face_recognition.compare_faces(face_encodings_list,faces)
            if matches[0] == True:
                video.release()
                speak('face matched')
                cv2.destroyAllWindows()
                run.startNick()


            else:
                speak('face not matched')
                speak('try again')
    
    cv2.imshow('Face Scan',frame)

    if cv2.waitkey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()