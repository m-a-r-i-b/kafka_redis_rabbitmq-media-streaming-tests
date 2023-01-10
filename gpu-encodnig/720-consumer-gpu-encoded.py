import pika
import numpy as np
import cv2
import time
import functools
import sys
from nvjpeg import NvJpeg
nj = NvJpeg()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

def callback(ch, method, properties, message, args):
    timingObject = args

    t1 = time.time()
    image = nj.decode(message)
    t2 = time.time()
    timingObject['totalTimeImgDecode'] += (t2-t1)


    timeStart = float(properties.headers['startTime'])
    timeEnd = time.time()
    timingObject['totalTimeEnd2End'] += (timeEnd-timeStart)


    timingObject['frameCount'] += 1
    cv2.imshow("image", image)
    cv2.waitKey(1)

    print(f'Average image decoding time  = {round(timingObject["totalTimeImgDecode"]/timingObject["frameCount"],5)}')
    print(f'Average end to end time      = {round(timingObject["totalTimeEnd2End"]/timingObject["frameCount"],5)}')
    print(f'Average end to end fps       = {round(1/(timingObject["totalTimeEnd2End"]/timingObject["frameCount"]),5)}')
    print('-'*20)



timingObject = {
    'frameCount': 0,
    'totalTimeBytesToFrame': 0,
    'totalTimeImgDecode': 0,
    'totalTimeEnd2End': 0,
}

on_message_callback = functools.partial(callback, args=(timingObject))
channel.basic_consume(queue='car1-queue', on_message_callback=on_message_callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
