#need to install firefox
# selenium, unidecode

from google import google, images

options = images.ImageOptions()
#options.image_type = images.ImageType.LINE_DRAWING
#options.format =
results = google.search_images("banana svg", options)
print results

for result in results:
    if result.link[-4:] == '.svg':
        images.download([result], path = "images/")
        print "downloaded image"
