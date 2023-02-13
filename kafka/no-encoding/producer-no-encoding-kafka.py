from confluent_kafka import Producer
import time
import cv2


config = {'bootstrap.servers': 'localhost:9092', 'message.max.bytes': '20000000'}

producer = Producer(config)


img1 = cv2.imread('../../720p_Images/1.jpg')
img2 = cv2.imread('../../720p_Images/2.jpg')
img3 = cv2.imread('../../720p_Images/3.jpg')
imgArr = [img1,img2,img3]

# cap = cv2.VideoCapture(0)
frameCount = 0
totalTimeFrameToBytes = 0
totalTimeMsgPublish = 0

while True:

    cycleTimeStart = time.time()

    # ret, frame = cap.read()
    frame = imgArr[frameCount%3]

    currTimeBytes = str(time.time()).encode('utf8')

    t1 = time.time()
    framebytes = frame.tobytes()
    # len(framebytes) == 2764800
    t2 = time.time()
    totalTimeFrameToBytes += (t2-t1)


    t11 = time.time()
    producer.produce(
        topic="multi-video-stream", 
        value=framebytes+currTimeBytes
    )
    producer.flush()
    t22 = time.time()
    totalTimeMsgPublish += (t22-t11)


    frameCount += 1


    print(f'Average frame to bytes time  = {round(totalTimeFrameToBytes/frameCount,5)}')
    print(f'Average message publish time = {round(totalTimeMsgPublish/frameCount,5)}')
    print('-'*20)

    cycleTimeEnd = time.time()
    oneCycleTime = cycleTimeEnd-cycleTimeStart
    # Cap producer to 30 fps, otherwise producer overruns consumer
    if oneCycleTime < (1/30):
        time.sleep((1/30)-oneCycleTime)
