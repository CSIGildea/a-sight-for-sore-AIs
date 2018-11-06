import face_recognition
import cv2
from bitarray import bitarray
import math
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture('5050_trailer.mp4')

# Load a sample picture and learn how to recognize it.
known_image = face_recognition.load_image_file("test_joseph.jpg")
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
frame_count = 0
frames = []
fps = video_capture.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
frameCount = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frameCount/fps
print('fps = ' + str(fps))
print('number of frames = ' + str(frameCount))
print('duration (S) = ' + str(duration))

duration = int(round(duration))
print(duration)

bitset = bitarray(duration*2)
bitset.setall(False)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Bail out when the video file ends
    if not ret:
        break
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    frame = small_frame[:, :, ::-1]

    # Save each frame of the video to a list
    frame_count += 1
    frames.append(frame)

    # Every 128 frames (the default batch size), batch process the list of frames to find faces
    if len(frames) == int(fps):
        print("frames",fps)
        batch_of_face_locations = face_recognition.batch_face_locations(frames, number_of_times_to_upsample=0)
        print("fast r nah?")


        # Now let's list all the faces we found in all 128 frames
        for frame_number_in_batch, face_locations in enumerate(batch_of_face_locations):
            found = False
            face_encodings = face_recognition.face_encodings(frames[frame_number_in_batch],face_locations)
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([known_face_encoding], face_encoding)
                if True in matches:
                    found = True
                    print("Found")
                    break
            if found:
                break

        # Clear the frames array to start the next batch
        frames = []

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
