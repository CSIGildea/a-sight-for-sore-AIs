import cv2
vidcap = cv2.VideoCapture('5050_trailer.mp4')

def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
	gray_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imwrite("test/frame "+str(sec)+" sec.jpg", gray_img)     # save frame as JPG file
    return hasFrames

sec = 0
frameRate = 1
success = getFrame(sec)
while success:
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)
