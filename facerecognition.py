import cv2
import face_recognition

vidcap = cv2.VideoCapture('5050_trailer.mp4')
face_csc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
known_celebrity = face_recognition.load_image_file("test_joseph.jpg")
known_celebrity_encoding = face_recognition.face_encodings(known_celebrity)[0]

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,frame = vidcap.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    new_frame  = small_frame[:,:,::-1]
    if hasFrames:
	face_locations = face_recognition.face_locations(new_frame)
        face_encodings = face_recognition.face_encodings(new_frame,face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_celebrity_encoding, face_encoding)
            if True in matches:
                print("%d Ladies and gentlemen...we got him!",sec)
            else:
                print("%d Nope soz!",sec)
                
    return hasFrames

sec = 0
frameRate = 1
success = getFrame(sec)
while success:
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)

cv2.destroyAllWindows()
