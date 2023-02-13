import pika
import cv2
import time
from nvjpeg import NvJpeg
nj = NvJpeg()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

channel.queue_declare(queue='car1-queue')

channel.queue_bind(exchange='direct_logs',
                   queue='car1-queue',
                   routing_key='car1')


img1 = cv2.imread('../../720p_Images/1.jpg')
img2 = cv2.imread('../../720p_Images/2.jpg')
img3 = cv2.imread('../../720p_Images/3.jpg')
imgArr = [img1,img2,img3]

frameCount = 0
totalFrameBytes = 0
totalTimeImgEncode = 0
totalTimeFrameToBytes = 0
totalTimeMsgPublish = 0

while True:

    cycleTimeStart = time.time()
    frame = imgArr[frameCount%3]

    startTime = str(time.time())

    t1 = time.time()
    frameBytes = nj.encode(frame)
    totalFrameBytes += len(frameBytes)
    t2 = time.time()
    totalTimeImgEncode += (t2-t1)


    t111 = time.time()
    channel.basic_publish(exchange='direct_logs',
                    routing_key='car1',
                    properties=pika.BasicProperties(
                        headers={'startTime': startTime} 
                    ),
                    body=frameBytes)
    t222 = time.time()
    totalTimeMsgPublish += (t222-t111)

    frameCount += 1

    print(f'Average frame encoding time  = {round(totalTimeImgEncode/frameCount,5)}')
    print(f'Average enocded frame bytes  = {round(totalFrameBytes/frameCount,5)}')
    print(f'Average message publish time = {round(totalTimeMsgPublish/frameCount,5)}')
    print('-'*20)

    cycleTimeEnd = time.time()
    oneCycleTime = cycleTimeEnd-cycleTimeStart
    # Cap producer to 30 fps, otherwise producer overruns consumer
    if(oneCycleTime < (1/30)):
        time.sleep((1/30)-oneCycleTime)