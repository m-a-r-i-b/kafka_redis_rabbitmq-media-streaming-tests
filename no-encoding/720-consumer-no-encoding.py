import pika
import numpy as np
import cv2
import time
import functools


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

def callback(ch, method, properties, message, args):

    timingObject = args


    # We know 720 frame == 2764800 bytes
    # 720*1280*24 == 22118400 bits == 2764800 bytes
    # So we split first 2764800 bytes to extract img and remaining bytes are decoded as message
    frameBytes = message[:2764800]
    startTimeBytes = message[2764800:]

    t1 = time.time()
    np_array = np.frombuffer(frameBytes, dtype=np.uint8)
    np_array = np_array.reshape(((720,1280,3)))
    image = np_array
    t2 = time.time()
    timingObject['totalTimeBytesToFrame'] += (t2-t1)


    timeStart = float(startTimeBytes.decode('utf-8'))
    timeEnd = time.time()
    timingObject['totalTimeEnd2End'] += (timeEnd-timeStart)


    timingObject['frameCount'] += 1
    cv2.imshow("image", image)
    cv2.waitKey(1)

    print(f'Average bytes to frame time  = {round(timingObject["totalTimeBytesToFrame"]/timingObject["frameCount"],5)}')
    print(f'Average end to end time      = {round(timingObject["totalTimeEnd2End"]/timingObject["frameCount"],5)}')
    print(f'Average end to end fps       = {round(1/(timingObject["totalTimeEnd2End"]/timingObject["frameCount"]),5)}')
    print('-'*20)
    



timingObject = {
    'frameCount': 0,
    'totalTimeBytesToFrame': 0,
    'totalTimeEnd2End': 0,
}

on_message_callback = functools.partial(callback, args=(timingObject))
channel.basic_consume(queue='car1-queue', on_message_callback=on_message_callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
