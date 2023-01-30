import static as static

import gxipy as gx
import numpy
import cv2
import easymodbus.modbusClient as MBus
import time
import threading
from collections import deque
from Cam import Camera
from PLC import modbusPLC


#nesne merkezi
buffer_size = 16
pts = deque(maxlen= buffer_size)

white_lower = (84, 98, 0)
white_upper = (179, 255, 255)

# set cam params
__ExposureTime = 1000.0
__Gain = 15.0

plcAddrs = '10.0.0.41'
plcPort = 502
addr_METRE_BILGISI = 160
addr_STOP_PLC = 34



def main():
    _threatStatus = True

    # create a device manager
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()
    if dev_num == 0:
        print("Number of enumerated devices is 0")
        return

    print("Number of Cam = " + str(dev_num))

    for i in range(dev_num):
        print("Camera " + str(i + 1) + " opened...")
        thr = threading.Thread(target=processImage, args=(i+1, __ExposureTime, __Gain))
        thr.start()
        time.sleep(1)



def processImage(__camindex, __ExposureTime, __Gain):
    while main._threatStatus:

        # görüntü alalım.
        Camera.camIndex = __camindex
        Camera.ExposureTime = __ExposureTime
        Camera.Gain = __Gain
        rgb_image = Camera.capture(Camera)
        print("image processing from camera -" + str(__camindex))


        # create numpy array with data from raw image
        numpy_image = rgb_image.get_numpy_array()
        if numpy_image is None:
            print("Getting image failed." + time.ctime(time.time()))

        # display image with opencv
        pimg = cv2.cvtColor(numpy.asarray(numpy_image), cv2.COLOR_BGR2RGB)
        pimg = cv2.resize(pimg, (720, 540))

        # blur
        blurred = cv2.GaussianBlur(pimg, (11, 11), 0)

        # hsv convert
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # maskeleme
        mask = cv2.inRange(hsv, white_lower, white_upper)

        # gürültü temizleme
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # kontur
        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:

            try:
                modbusPLC.plcIP = str(plcAddrs)
                modbusPLC.plcPort = plcPort
                modbusPLC.addr_METRE_BILGISI = addr_METRE_BILGISI
                modbusPLC.addr_STOP_PLC = addr_STOP_PLC
                modbusPLC.setPLC(modbusPLC)
            except:
                print("PLC Connection ERROR ! " + time.ctime(time.time()))

            main._threatStatus = False
            break



main()




