import speech_recognition as sr

import contour

from google import google, images

options = images.ImageOptions()
options.image_type = images.ImageType.LINE_DRAWING

from os import listdir

#options.format =

import threading

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        #text =  recognizer.recognize_sphinx(audio)
        text =  recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said " +text)
        if len(text.split())>=2:
            request = text.split()[-2:]
        else:
            request = [text]
        results = google.search_images(' '.join(request), options)
        print results
        '''
        for result in results:
            if result.link[-4:] == '.svg':
                images.download([result], path = "images/"+ '_'.join(request))
                print "downloaded image"
                break
        '''
        filepath = "images/"+ '_'.join(request)
        images.download([results[0]], path = filepath)
        filename = listdir(filepath)[0]
        #stop_listening()
        contour.show_contour(filepath+'/'+filename)
        #t = threading.Thread(target=contour.show_contour, args=(filepath+'/'+filename,))
        #t.start()
        #r.listen_in_background(m, callback)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

r.pause_threshold = 0.2
r.non_speaking_duration = r.pause_threshold - 0.1
# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some other computation for 5 seconds, then stop listening and keep doing other computations
import time
for _ in range(50): time.sleep(0.1) # we're still listening even though the main thread is doing other things
#print "didn't find nothing"
#stop_listening() # calling this function requests that the background listener stop listening
while True: time.sleep(0.1)
