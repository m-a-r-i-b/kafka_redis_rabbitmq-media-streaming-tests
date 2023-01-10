import pika
import cv2
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

channel.queue_declare(queue='car1-queue')

channel.queue_bind(exchange='direct_logs',
                   queue='car1-queue',
                   routing_key='car1')


img1 = cv2.imread('../720p_Images/1.jpg')
img2 = cv2.imread('../720p_Images/2.jpg')
img3 = cv2.imread('../720p_Images/3.jpg')
imgArr = [img1,img2,img3]


frameCount = 0
totalTimeFrameToBytes = 0
totalTimeMsgPublish = 0

while True:

    cycleTimeStart = time.time()
    frame = imgArr[frameCount%3]

    currTimeBytes = str(time.time()).encode('utf8')

    t1 = time.time()
    framebytes = frame.tobytes()
    # len(framebytes) == 2764800
    t2 = time.time()
    totalTimeFrameToBytes += (t2-t1)


    t11 = time.time()
    channel.basic_publish(exchange='direct_logs',
                    routing_key='car1',
                    body=framebytes+currTimeBytes)
    t22 = time.time()
    # Even tho this is an async function, its time still scales with number of bytes
    totalTimeMsgPublish += (t22-t11)

    frameCount += 1

    print(f'Average frame to bytes time  = {round(totalTimeFrameToBytes/frameCount,5)}')
    print(f'Average message publish time = {round(totalTimeMsgPublish/frameCount,5)}')
    print('-'*20)

    cycleTimeEnd = time.time()
    oneCycleTime = cycleTimeEnd-cycleTimeStart
    # Cap producer to 30 fps, otherwise producer overruns consumer
    time.sleep((1/30)-oneCycleTime)
