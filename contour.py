import numpy as np
import cv2

def show_contour(filename):
    im = cv2.imread(filename)
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)


    #Tighten up threshold to avoid watermarks
    ret,thresh = cv2.threshold(imgray,200,255,0)
    #thresh = cv2.Canny(imgray,100,200)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print hierarchy
    #**[Next, Previous, First_Child, Parent]**

    empty = np.zeros(im.shape,np.uint8)
    empty2 = np.zeros(im.shape,np.uint8)
    #To remove border. This is bad if image touches boundaries. Buffer image?
    ymax = 1000.
    xmax = 1000.
    scale = min(ymax/im.shape[0], xmax/im.shape[1])


    for i in range(len(contours)):
        if hierarchy[0,i,3] != -1:
            cv2.drawContours(empty,contours,i,(0,255,0),1)
    #cv2.imshow('res',empty)
    cv2.drawContours(empty2,contours,-1,(0,255,0),1)
    #cv2.imshow('butt',empty2)
    #if cv2.waitKey(0) & 0xff == 27:
#        cv2.destroyAllWindows()
    writename = '/'.join(filename.split('/')[:-1]) + '/' + 'contour.jpg'
    cv2.imwrite(writename,empty)
#show_contour('images/bird_bird/bird-skeleton-big.jpg')
