from confluent_kafka import Producer
import time
import cv2
from nvjpeg import NvJpeg
nj = NvJpeg()

config = {'bootstrap.servers': 'localhost:9092', 'message.max.bytes': '20000000'}

producer = Producer(config)


img1 = cv2.imread('../../720p_Images/1.jpg')
img2 = cv2.imread('../../720p_Images/2.jpg')
img3 = cv2.imread('../../720p_Images/3.jpg')
imgArr = [img1,img2,img3]

frameCount = 0
totalTimeImgEncode = 0 
totalFrameBytes = 0
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
    producer.produce(
        topic="multi-video-stream", 
        value=frameBytes,
        headers={'startTime': startTime} 
    )
    producer.flush()
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
    if oneCycleTime < (1/30):
        time.sleep((1/30)-oneCycleTime)
