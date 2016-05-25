import cv2
import numpy as np


class PhotoConverter:

    def __init__(self):
        self.fraction = 16 # 1/fraction largest area contours are drawn
        self.openCamera()
        self.robotFraction = 0.25 #Full Range of x is 1600, y is 1200


    def openCamera(self):
        self.cap = cv2.VideoCapture(0)
        _, frame = self.cap.read()
    def closeCamera(self):
        self.cap.release()

    def setDrawFraction(self, newfrac):
        self.robotFraction = newfrac

    def squareFrame(self,frame):
        if frame.shape[0] < frame.shape[1]:
            offset = int((frame.shape[1]-frame.shape[0])/2)
            return frame[:,offset:frame.shape[0]-offset]
        else:
            offset = int((frame.shape[0]-frame.shape[1])/2)
            return frame[offset:frame.shape[1]-offset,:]


    def takePhoto(self):
        #Take photo, convert to gray, downsample, threshold, find contours
        _, frame = self.cap.read()
        self.frame = self.squareFrame(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = self.findFace(gray)
        gray = cv2.pyrDown(gray)

        self.h = gray.shape[0]
        self.w = gray.shape[1]
        
        self.thres = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2)
        self.contours,self.hierarchy = cv2.findContours(self.thres,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #Order contours by area
        area = np.asarray(map(cv2.contourArea, self.contours))
        self.indexorder = np.argsort(area)[::-1]
        self.contours = np.array(self.contours)
        self.contours = self.contours[self.indexorder[: int(len(self.contours)/self.fraction)]]


    def drawContours(self):
        newempty = np.ones((self.h,self.w,3), dtype=np.uint8)
        for i in range(len(self.contours)):
            cv2.drawContours(newempty, self.contours, i, (0,0,255), 1)
        #Simplified triangles
        cv2.imshow('Contours',newempty)
        k = cv2.waitKey(0)
        cv2.destroyAllWindows()

    def saveContour(self, filename):
        newempty = np.ones((self.h,self.w,3), dtype=np.uint8)
        for i in range(len(self.contours)):
            cv2.drawContours(newempty, self.contours, i, (0,0,255), 1)
        cv2.imwrite(filename, newempty)

    '''
    def scaleContours(self, w, h):
        xmax = 0
        ymax = 0
        w = float(w)
        h = float(h)

        scale = self.robotFraction * min(w / self.w, h / self.h)
        offsetx = (w - scale*self.w)/2
        offsety =  (h - scale*self.h)/2

        for cnt in self.contours:
            for point in cnt:
                point = point[0]
                point[0] = int(point[0] * scale + offsetx)
                point[1] = int(point[1] * scale + offsety)
        self.w = w #int(self.w * scale)
        self.h = h #int(self.h * scale)
        print self.contours
    '''
    #x = 630
    #y = 480
    #w = 370
    #h = 370
    def scaleContours(self, x=630, y=480, w=370, h=370):

        
        xmax = 0
        ymax = 0
        w = float(w)
        h = float(h)

        scale = min(w / self.w, h / self.h)
        offsetx = x#(w - scale*self.w)/2
        offsety =  y#(h - scale*self.h)/2

        for cnt in self.contours:
            for point in cnt:
                point = point[0]
                point[0] = int(point[0] * scale + offsetx)
                point[1] = int((self.h-point[1]) * scale + offsety)
        self.w = w #int(self.w * scale)
        self.h = h #int(self.h * scale)
        print self.contours

    def sortContours(self):
        temp = []
        unused = np.copy(self.contours)
        temp.append(self.contours[0])

        def rotateList(l,n): #cyclically roatets the list l so that the n index position is now at index 0
            return np.concatenate((l[n:],l[:n]))

        for i in range(1,len(self.contours)):
            closestdist = 10000000000
            closestcontourindex = 0
            lastpoint = temp[i-1][0] #where the pen is after drawing i-1 contour

            dists =  map(lambda cnt: (cnt[:,0,0]-lastpoint[0][0])**2 + (cnt[:,0,1]-lastpoint[0][1])**2, unused)
            minofcnt = np.asarray(map(lambda cnt:  np.amin(cnt), dists))
            closestcontourindex = np.argmin(minofcnt)
            firstpointindex = np.argmin(dists[closestcontourindex])

            closestcnt = unused[closestcontourindex]
            unused = np.delete(unused, closestcontourindex , axis=0)
            temp.append(rotateList(closestcnt, firstpointindex))


        self.contours = np.asarray(temp)





    def saveFrame(self,filename):
        cv2.imwrite(filename, self.frame)


    def convertContourstoGcode(self):
        raisepen = "M05\r\n"
        lowerpen = "M03\r\n"
        def move(x,y):
            return "G1 X" + str(x) + " Y" + str(y) + "\r\n"

        gcode = ""
        #for cnt in self.contours[self.indexorder]: #format of contour is [ [[x y]], [[x,y]] ] Why they put double array in there god knows
        #for i in range(int(len(self.indexorder)/self.fraction)):
        for i in range(len(self.contours)):
            #cnt = self.contours[self.indexorder[i]]
            cnt = self.contours[i]
            gcode += raisepen   # Also dule note that i needed to convert contours to numpy array to index like this
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
