import face_recognition
import cv2
import math
import csv
from multiprocessing import Pool, Array
import time

# Load video to process
video_capture = cv2.VideoCapture('video1.mp4')
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
    if arr[frame[1]]:
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
            arr[frame[1]] = 1
            return frame[1]

def init(local_arr):
    global arr
    arr = local_arr

# Get video information. Used to know what second the frame appears in
fps = video_capture.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
frameCount = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
duration = int(round(frameCount/fps))

print('fps = ' + str(fps))
print('number of frames = ' + str(frameCount))
print('duration (S) = ' + str(duration))

start_time = time.time()

frameRate = 0.25
sec = 0
while sec<(duration+1):
   getFrame(sec)
   if sec % 100 == 0:
       print(sec)
   sec = round((sec + frameRate), 2)

# Create the threads to run checkFace
arr = Array('i', range(2,duration+3), lock=False)
pool = Pool(initializer=init, initargs=(arr,))
results = pool.map(checkFace,frames)

# Close the pool and wait for the work to finish
pool.close()
pool.join()

# Write results to answers.csv
data = []
for i in range(len(arr)):
    if arr[i]!=1:
        arr[i] = 0
    data.append([i,arr[i]])

with open("answers.csv", "wb") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print(time.time() - start_time)
print("Done...")

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
