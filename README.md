# RabbitMQ - Media Streaming Tests
This repo contains 3 producer-consumer pair of test scripts. Each producer emits out a frame of 720p@30fps, digested by the consumer and displayed to user. The 3 producer-consumer configrations are as follows: 

Results of these experiments are available <a href="https://docs.google.com/spreadsheets/d/1H4yaXyhLMSXv95ZCG8Gy7YiYUVs9MED7or3xUwP9l04/edit?usp=sharing">here</a>

![results-img](https://user-images.githubusercontent.com/77619505/211660884-02273a8f-a68e-44b5-bb27-77904a3eb52a.png)

### Config 1 - No Encoding
The folder 'no-encoding' contains producer-consumer script pair where producer reads 720p frames, converts them to bytes and directs them to the consumer where they are converted back to a frame from byte string and then displayed.
![no-encoding-img](https://user-images.githubusercontent.com/77619505/211660969-d6bf99a0-2d42-4e7a-855d-b530f4f1468d.png)


### Config 2 - CPU Encoding
The folder 'cpu-encoding' contains producer-consumer script pair where producer reads 720p frames, <b>encodes them on CPU using OpenCV</b> and converts them to bytes and directs them to the consumer where they are converted back to a frame from byte string, <b>decoded</b> and then displayed.


### Config 3 - GPU Encoding
The folder 'gpu-encoding' contains producer-consumer script pair where producer reads 720p frames, <b>encodes them on GPU using nvJPEG</b> and directs them to the consumer where they are <b>decoded</b> and then displayed.




### To run a test
```
# Step 1 - Start rabbitmq container
./spinContainer.sh

# Step 2 - Start consumer process
cd cpu-encoding/
python 720-consumer-cpu-encoded.py

# Step 3 - Start producer process
720-consumer-cpu-encoded.py
```
