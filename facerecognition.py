import cv2
import face_recognition

vidcap = cv2.VideoCapture('5050_trailer.mp4')
face_csc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
known_celebrity = face_recognition.load_image_file("test_joseph.jpeg")
known_celebrity_encoding = face_recognition.face_encodings(known_celebrity)[0]

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
	gray_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	face_locations = face_recognition.face_locations(grey_img)
	for face_location in face_locations:
	    face_encoding = face_recognition.face_encodings(face_location)[0]
    	    results = face_recognition.compare_faces([known_celebrity_encoding], unknown_face_encoding)

	    if results[0] == True:
    	        print("%dLadies and gentlemen....we got him!",sec)
	    else:
                print("%dNo known celebrity here!",sec)
    return hasFrames

sec = 0
frameRate = 1
success = getFrame(sec)
while success:
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)

cv2.destroyAllWindows()
