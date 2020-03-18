import cv2
import time

def countdown(t):
    while t>0:
        print(t)
        t=t-1
        time.sleep(1)
    print('Clicking!')
    
countdown(2)

video_capture = cv2.VideoCapture(0)
# Check success
if not video_capture.isOpened():
    raise Exception("Could not open video device")
# Read picture. ret === True on success
ret, frame = video_capture.read()
# Close device
video_capture.release()

import sys
from matplotlib import pyplot as plt

frameRGB = frame[:,:,::-1] # BGR => RGB
plt.imshow(frameRGB)

#Save the captured image
from PIL import Image
import numpy as np
im = Image.fromarray(frameRGB)
im.save('./cam_pics/test.png')


#Checking the object in image
from keras.models import load_model


model_path = 'modeln.h5'
model_weights_path = 'modeln_weights.h5'
test_path = './test'


new_model = load_model(model_path)
new_model.load_weights(model_weights_path)

img_width, img_height = 64, 64

import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
def predict(p):
    p = img_to_array(p)
    p = np.expand_dims(p, axis=0)
    array = new_model.predict(p)
    result = array[0]
    answer = np.argmax(result)
    return answer

def classify(c):
    if c==0:
        c_img='Bandaid'
    elif c==1:
        c_img="Bottle"
    elif c==2:
        c_img="Cloth"
    elif c==3:
        c_img="Guns"
    elif c==4:
        c_img="Shelling"
    elif c==5:
        c_img="Syringe"
    print(c_img)

#Testing
x = load_img('./cam_pics/test.png', target_size=(img_width,img_height))
ans = predict(x)
classify(ans)

#Sending data
from urllib.request import urlopen
connection2 = urlopen("https://api.thingspeak.com/update?api_key=R9OCBK0BVSOT65QB&field2="+str(ans))
if connection2:
	print("2 Sent Successfully")
else:
	print("Failed")