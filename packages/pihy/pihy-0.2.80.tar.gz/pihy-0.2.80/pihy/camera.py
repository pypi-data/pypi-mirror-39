import picamera
import time
import json
import os

storage_path = "/var/www/dist/logs/camera.json"
timeStart = time.strftime("%Y-%m-%d %H:%M:%S")

camera = picamera.PiCamera()
camera.resolution = (2592, 1944)

camera.start_preview()
camera.annotate_background = picamera.Color('blue')
camera.annotate_foreground = picamera.Color('yellow')
camera.annotate_text = "Time: %s" % timeStart
camera.annotate_text_size = 50
time.sleep(5)

camera.capture('/var/www/dist/camera/image.jpg')
camera.stop_preview()

camera.close()

data = None
if os.path.exists(storage_path):
    with open(storage_path,'r') as f:
        try:
            data = json.load(f)
            print('loaded that: ',data)
        except Exception as e:
            print("got %s on json.load()" % e)


if data is None:
    print('Create new dataset')
    data = [ ]

data.append(timeStart)

with open(storage_path, 'w') as outfile:
    json.dump(data, outfile)



