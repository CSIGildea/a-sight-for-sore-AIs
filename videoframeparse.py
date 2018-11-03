import cv2
vidcap = cv2.VideoCapture('5050_trailer.mp4')
face_csc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
	gray_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	cv2.imshow('window-name',gray_img)
	faces = face_csc.detectMultiScale(gray_img, 1.1, 4)
    
    	for (x, y, w, h) in faces:
            cv2.rectangle(gray_img, (x,y), (x+w, y+h), (0,0,0), 5)
        
    	cv2.imshow('img', gray_img)
    	key = cv2.waitKey(1)
    	#cv2.imwrite("frame%d.jpg" % count, frame)
        #cv2.imwrite("test/frame "+str(sec)+" sec.jpg", gray_img)     # save frame as JPG file
    return hasFrames

sec = 0
frameRate = 1
success = getFrame(sec)
while success:
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)

cv2.destroyAllWindows()
