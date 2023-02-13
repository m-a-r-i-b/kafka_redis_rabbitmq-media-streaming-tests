from confluent_kafka import Consumer, OFFSET_END,TopicPartition,OFFSET_BEGINNING
import cv2
import numpy as np
import time


topic = ["multi-video-stream"]
config = {
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'msssse',
    'enable.auto.commit': False,
    'default.topic.config': {'auto.offset.reset': 'latest'}
}

consumer = Consumer(config)
consumer.assign([TopicPartition(topic[0], 0,OFFSET_END)])

frameCount = 0
totalTimeBytesToFrame = 0
totalTimeEnd2End = 0

while True:
    print("Polling")
    msg = consumer.poll()

    if msg == None:
        continue

    message = msg.value()
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
    totalTimeBytesToFrame += (t2-t1)

    timeStart = float(startTimeBytes.decode('utf-8'))
    timeEnd = time.time()
    totalTimeEnd2End += (timeEnd-timeStart)


    frameCount += 1
    cv2.imshow("image", image)
    cv2.waitKey(1)

    print(f'Average bytes to frame time  = {round(totalTimeBytesToFrame/frameCount,5)}')
    print(f'Average end to end time      = {round(totalTimeEnd2End/frameCount,5)}')
    print(f'Average end to end fps       = {round(1/(totalTimeEnd2End/frameCount),5)}')
    print('-'*20)

