import face_recognition
import cv2
from bitarray import bitarray
import math
import csv
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process, Queue
import random, time, difflib
from random import shuffle

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture('5050_trailer.mp4')
frames = []
# Load a sample picture and learn how to recognize it.
known_image = face_recognition.load_image_file("test_joseph.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]

def getFrame(sec):
    video_capture.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    # Grab a single frame of video
    ret, fr = video_capture.read()

    if ret:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_fr = cv2.resize(fr, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_fr[:, :, ::-1]
        frames.append([rgb_small_frame,int(math.ceil(sec))])
    return ret

def checkFace(frame):
    if bitset[frame[1]]:
        return
    # Find all the faces and face encodings in the current frame of video
    #face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = []
    face_encodings = face_recognition.face_encodings(frame[0])

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces([known_face_encoding], face_encoding)
        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            print("Found: ",frame[1])
            bitset[frame[1]] = 1
            return True



fps = video_capture.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
frameCount = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frameCount/fps
print('fps = ' + str(fps))
print('number of frames = ' + str(frameCount))
print('duration (S) = ' + str(duration))

duration = int(round(duration))
print(duration)
bitset = bitarray(duration+1)
bitset.setall(False)

t = time.time()
frameRate = 0.25
seconds = []
sec = 0
while sec<(duration+1):
    seconds.append(sec)
    getFrame(sec)
    print(sec)
    sec = sec + frameRate
    sec = round(sec, 2)

pool = Pool()
pool.map(checkFace,frames)
#close the pool and wait for the work to finish
pool.close()
pool.join()
print time.time()-t
print("Done...")


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
