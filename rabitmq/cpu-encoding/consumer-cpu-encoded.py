import pika
import numpy as np
import cv2
import time
import functools
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

def callback(ch, method, properties, message, args):

    timingObject = args

    t1 = time.time()
    size = sys.getsizeof(message) - 33
    np_array = np.frombuffer(message, dtype=np.uint8)
    np_array = np_array.reshape((size,1))
    t2 = time.time()
    timingObject['totalTimeBytesToFrame'] += (t2-t1)

    t11 = time.time()
    image = cv2.imdecode(np_array, 1)
    t22 = time.time()
    timingObject['totalTimeImgDecode'] += (t22-t11)


    timeStart = float(properties.headers['startTime'])
    timeEnd = time.time()
    timingObject['totalTimeEnd2End'] += (timeEnd-timeStart)


    timingObject['frameCount'] += 1
    cv2.imshow("image", image)
    cv2.waitKey(1)

    print(f'Average bytes to frame time  = {round(timingObject["totalTimeBytesToFrame"]/timingObject["frameCount"],5)}')
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
