from PhotoConverter import PhotoConverter 
import time

mydude = PhotoConverter()
mydude.takePhoto()
mydude.drawContours()
mydude.sortContours()
mydude.drawContours()
mydude.scaleContours(1600,1200)
mydude.drawContours()
#print mydude.convertContourstoGcode()
#mydude.simplifyContours()
#mydude.drawContours()

