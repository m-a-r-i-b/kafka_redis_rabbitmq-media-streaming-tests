from confluent_kafka import Consumer, OFFSET_END,TopicPartition,OFFSET_BEGINNING
import cv2
import numpy as np
import time
import sys
import redis
from nvjpeg import NvJpeg
nj = NvJpeg()

topic = ["multi-video-stream"]
config = {
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'msssse',
    'enable.auto.commit': False,
    'default.topic.config': {'auto.offset.reset': 'latest'}
}

consumer = Consumer(config)
consumer.assign([TopicPartition(topic[0], 0,OFFSET_END)])
redisClient = redis.Redis(host='localhost', port=6379)

frameCount = 0
totalTimeEnd2End = 0
totalTimeImgDecode = 0

while True:
    print("Polling")
    msg = consumer.poll()

    if msg == None:
        continue
    
    message = msg.value()
    frameKey = message.decode()
    encodedFrame = redisClient.get(frameKey)

    t1 = time.time()
    image = nj.decode(encodedFrame)
    t2 = time.time()
    totalTimeImgDecode += (t2-t1)

    timeStart = float(redisClient.get(frameKey+'_T'))
    timeEnd = time.time()
    totalTimeEnd2End += (timeEnd-timeStart)


    frameCount += 1
    cv2.imshow("image", image)
    cv2.waitKey(1)

    print(f'Average image decoding time  = {round(totalTimeImgDecode/frameCount,5)}')
    print(f'Average end to end time      = {round(totalTimeEnd2End/frameCount,5)}')
    print(f'Average end to end fps       = {round(1/(totalTimeEnd2End/frameCount),5)}')
    print('-'*20)

