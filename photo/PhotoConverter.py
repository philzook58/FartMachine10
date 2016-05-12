import cv2
import numpy as np


class PhotoConverter:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.fraction = 16 # 1/fraction largest area contours are drawn
        _, frame = self.cap.read() #get the camera juicin'


    def takePhoto(self):
        #Take photo, convert to gray, downsample, threshold, find contours
        _, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = self.findFace(gray)
        gray = cv2.pyrDown(gray)
        self.thres = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2)
        self.contours,self.hierarchy = cv2.findContours(self.thres,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        #Order contours by area
        i=0
        area = np.zeros(len(self.contours))
        for cnt in self.contours:
            area[i] = cv2.contourArea(cnt)
            i=i+1
            self.indexorder = np.argsort(area)[::-1]

    def drawContours(self):
        newempty = np.ones((self.thres.shape[0],self.thres.shape[1],3), dtype=np.uint8)
        for i in range(int(len(self.indexorder)/self.fraction)):
            cv2.drawContours(newempty, self.contours, self.indexorder[i], (0,0,255), 1)
        #Simplified triangles
        cv2.imshow('Contours',newempty)
        k = cv2.waitKey(0)
        cv2.destroyAllWindows()

    def convertContourstoGcode(self):
        raisepen = "M05\n"
        lowerpen = "M03\n"
        def move(x,y):
            return "G1 X" + str(x) + " Y" + str(y) + "\n" 

        gcode = ""
        for cnt in self.contours: #format of contour is [ [[x y]], [[x,y]] ] Why they put double array in there god knows
            gcode += raisepen
            gcode += move(cnt[0][0][0],cnt[0][0][1])
            gcode += lowerpen
            for point in cnt:
                point = point[0]
                gcode += move(point[0],point[1])
        gcode += raisepen
        gcode += move(0,0)
        return gcode

    def simplifyContours(self,eps=0.001):
        for i in range(len(self.contours)):
            cnt = self.contours[i]
            epsilon = eps*cv2.arcLength(cnt,True)
            self.contours[i] = cv2.approxPolyDP(cnt,epsilon,True)

    def findFace(self,gray):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if faces: #Perhaps a better approach would be to blur using faces as crispness points? Might want mutiple faces
            faces = sorted(faces, key = lambda (x,y,w,h): w * h, reverse=True) #Also sort for largest faces rather than arbitrary face
            (x,y,w,h) = faces[0] 
            left = max(x-w/2,0)
            right = min(x+3*w/2,gray.shape[1])
            down = min(y+3*h/2,gray.shape[0])
            up = max(y-h/2,0)
            return gray[up:down, left:right] #Yes. The coordinate system of computers is goofy.
        else:
            return gray







