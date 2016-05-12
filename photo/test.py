from PhotoConverter import PhotoConverter 
import time

mydude = PhotoConverter()
mydude.takePhoto()
mydude.drawContours()
print mydude.convertContourstoGcode()
mydude.simplifyContours()
mydude.drawContours()

